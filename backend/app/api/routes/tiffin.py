import io
import uuid
from datetime import date as date_type

from fastapi import APIRouter, Depends, HTTPException, Response, status
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy import case, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models import Person, TiffinAction, TiffinLog, User
from app.db.session import get_db
from app.schemas.tiffin import GiveTiffinIn, TiffinLogOut, TiffinStatusOut, TiffinSummaryOut, UndoTiffinIn

router = APIRouter()


def _get_person_owned(db: Session, owner_id: uuid.UUID, person_id: uuid.UUID) -> Person:
    person = db.scalar(
        select(Person).where(Person.id == person_id, Person.owner_id == owner_id, Person.deleted_at.is_(None))
    )
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.post("/give", response_model=TiffinLogOut, status_code=status.HTTP_201_CREATED)
def give_tiffin(payload: GiveTiffinIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_person_owned(db, current_user.id, payload.person_id)

    log = TiffinLog(
        owner_id=current_user.id,
        person_id=payload.person_id,
        date=payload.date,
        action=TiffinAction.GIVEN,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return TiffinLogOut(
        id=log.id,
        person_id=log.person_id,
        date=log.date,
        action=log.action.value,
        created_at=log.created_at,
    )


@router.post("/undo", response_model=TiffinLogOut, status_code=status.HTTP_201_CREATED)
def undo_tiffin(payload: UndoTiffinIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_person_owned(db, current_user.id, payload.person_id)

    given_count = db.scalar(
        select(func.count()).select_from(TiffinLog).where(
            TiffinLog.owner_id == current_user.id,
            TiffinLog.person_id == payload.person_id,
            TiffinLog.date == payload.date,
            TiffinLog.action == TiffinAction.GIVEN,
        )
    )
    reversed_count = db.scalar(
        select(func.count()).select_from(TiffinLog).where(
            TiffinLog.owner_id == current_user.id,
            TiffinLog.person_id == payload.person_id,
            TiffinLog.date == payload.date,
            TiffinLog.action == TiffinAction.REVERSED,
        )
    )

    if (given_count or 0) <= (reversed_count or 0):
        raise HTTPException(status_code=409, detail="Cannot undo: all given entries for this date have been reversed or none exist")

    log = TiffinLog(
        owner_id=current_user.id,
        person_id=payload.person_id,
        date=payload.date,
        action=TiffinAction.REVERSED,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return TiffinLogOut(
        id=log.id,
        person_id=log.person_id,
        date=log.date,
        action=log.action.value,
        created_at=log.created_at,
    )


@router.get("/status", response_model=TiffinStatusOut)
def tiffin_status(date: date_type, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    persons = db.scalars(
        select(Person)
        .where(Person.owner_id == current_user.id, Person.deleted_at.is_(None))
        .order_by(Person.created_at.asc())
    ).all()
    if not persons:
        return {"date": date, "persons": []}

    person_ids = [p.id for p in persons]

    # Counts for selected date
    counts = db.execute(
        select(
            TiffinLog.person_id,
            func.sum(case((TiffinLog.action == TiffinAction.GIVEN, 1), else_=0)).label("given"),
            func.sum(case((TiffinLog.action == TiffinAction.REVERSED, 1), else_=0)).label("reversed"),
        )
        .where(
            TiffinLog.owner_id == current_user.id,
            TiffinLog.person_id.in_(person_ids),
            TiffinLog.date == date,
        )
        .group_by(TiffinLog.person_id)
    ).all()
    by_person_counts = {row[0]: {"given": int(row[1] or 0), "reversed": int(row[2] or 0)} for row in counts}

    # Totals lifetime
    totals = db.execute(
        select(
            TiffinLog.person_id,
            (
                func.sum(case((TiffinLog.action == TiffinAction.GIVEN, 1), else_=0))
                - func.sum(case((TiffinLog.action == TiffinAction.REVERSED, 1), else_=0))
            ).label("total"),
        )
        .where(TiffinLog.owner_id == current_user.id, TiffinLog.person_id.in_(person_ids))
        .group_by(TiffinLog.person_id)
    ).all()
    by_person_total = {row[0]: int(row[1] or 0) for row in totals}

    out = []
    for p in persons:
        c = by_person_counts.get(p.id, {"given": 0, "reversed": 0})
        out.append(
            {
                "id": p.id,
                "name": p.name,
                "age": p.age,
                "given_count": c["given"],
                "reversed_count": c["reversed"],
                "total_tiffins": by_person_total.get(p.id, 0),
            }
        )


    return {"date": date, "persons": out}


@router.get("/summary", response_model=TiffinSummaryOut)
def tiffin_summary(date: date_type, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 1. Month range
    start_of_month = date.replace(day=1)
    if date.month == 12:
        end_of_month = date.replace(year=date.year + 1, month=1, day=1)
    else:
        end_of_month = date.replace(month=date.month + 1, day=1)
    
    # 2. Total Tiffins This Month
    month_result = db.execute(
        select(
            func.sum(case((TiffinLog.action == TiffinAction.GIVEN, 1), else_=0))
            - func.sum(case((TiffinLog.action == TiffinAction.REVERSED, 1), else_=0))
        ).where(
            TiffinLog.owner_id == current_user.id,
            TiffinLog.date >= start_of_month,
            TiffinLog.date < end_of_month,
        )
    ).scalar()
    total_month = int(month_result or 0)

    # 3. Today's Given (Net)
    today_result = db.execute(
        select(
            func.sum(case((TiffinLog.action == TiffinAction.GIVEN, 1), else_=0))
            - func.sum(case((TiffinLog.action == TiffinAction.REVERSED, 1), else_=0))
        ).where(
            TiffinLog.owner_id == current_user.id,
            TiffinLog.date == date,
        )
    ).scalar()
    today_given = int(today_result or 0)

    # 4. Total Active Persons
    active_persons = db.scalar(
        select(func.count()).select_from(Person).where(
            Person.owner_id == current_user.id,
            Person.deleted_at.is_(None)
        )
    )

    return {
        "month_name": date.strftime("%B %Y"),
        "total_tiffins_this_month": total_month,
        "total_active_persons": active_persons or 0,
        "today_given": today_given,
    }


@router.get("/history/{person_id}", response_model=list[TiffinLogOut])
def tiffin_history(person_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_person_owned(db, current_user.id, person_id)

    logs = db.scalars(
        select(TiffinLog)
        .where(TiffinLog.owner_id == current_user.id, TiffinLog.person_id == person_id)
        .order_by(TiffinLog.date.asc(), TiffinLog.created_at.asc())
    ).all()

    return [
        TiffinLogOut(
            id=l.id,
            person_id=l.person_id,
            date=l.date,
            action=l.action.value,
            created_at=l.created_at,
        )
        for l in logs
    ]


@router.get("/pdf/{person_id}")
def tiffin_pdf(person_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    person = _get_person_owned(db, current_user.id, person_id)

    logs = db.scalars(
        select(TiffinLog)
        .where(TiffinLog.owner_id == current_user.id, TiffinLog.person_id == person_id)
        .order_by(TiffinLog.date.asc(), TiffinLog.created_at.asc())
    ).all()

    total = sum(1 if l.action == TiffinAction.GIVEN else -1 for l in logs)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Person Name: {person.name}")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Age: {person.age}")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, "----------------------------------")
    y -= 20
    c.drawString(50, y, "Date")
    c.drawString(200, y, "|")
    c.drawString(220, y, "Status")
    y -= 15
    c.drawString(50, y, "----------------------------------")
    y -= 20

    c.setFont("Helvetica", 10)
    for l in logs:
        if y < 80:
            c.showPage()
            y = height - 60
            c.setFont("Helvetica", 10)
        c.drawString(50, y, l.date.strftime("%d-%m-%Y"))
        c.drawString(200, y, "|")
        c.drawString(220, y, l.action.value)
        y -= 16

    y -= 10
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "----------------------------------")
    y -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Total Tiffins: {total}")

    c.showPage()
    c.save()

    pdf_bytes = buf.getvalue()
    buf.close()

    filename = f"tiffin_{person.name.replace(' ', '_')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename={filename}",
            "Cache-Control": "no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
