from fastapi import APIRouter

from app.api.routes import auth, persons, tiffin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(persons.router, prefix="/persons", tags=["persons"])
api_router.include_router(tiffin.router, prefix="/tiffin", tags=["tiffin"])
