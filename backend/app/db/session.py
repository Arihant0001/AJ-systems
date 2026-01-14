from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# Force IPv4 connection and add connection timeout
connect_args = {}

# For PostgreSQL, we can add connection options
if settings.database_url.startswith("postgresql"):
    connect_args = {
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000"
    }

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_size=5,
    max_overflow=10,
    connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
