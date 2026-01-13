import uuid

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models import Person, TiffinLog, User
from app.db.session import get_db
from app.schemas.persons import PersonCreateIn, PersonOut

router = APIRouter()


@router.get("", response_model=list[PersonOut])
def list_persons(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    persons = db.scalars(
        select(Person)
        .where(Person.owner_id == current_user.id, Person.deleted_at.is_(None))
        .order_by(Person.created_at.asc())
    ).all()
    return [PersonOut(id=p.id, name=p.name, age=p.age, created_at=p.created_at) for p in persons]


@router.post("", response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(payload: PersonCreateIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    person = Person(owner_id=current_user.id, name=payload.name, age=payload.age)
    db.add(person)
    db.commit()
    db.refresh(person)
    return PersonOut(id=person.id, name=person.name, age=person.age, created_at=person.created_at)


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    person = db.scalar(
        select(Person).where(Person.id == person_id, Person.owner_id == current_user.id, Person.deleted_at.is_(None))
    )
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    has_logs = db.scalar(
        select(exists().where(TiffinLog.owner_id == current_user.id, TiffinLog.person_id == person_id))
    )
    if has_logs:
        raise HTTPException(status_code=409, detail="Cannot delete person with tiffin history")

    person.deleted_at = datetime.now(timezone.utc)
    db.add(person)
    db.commit()
    return None
