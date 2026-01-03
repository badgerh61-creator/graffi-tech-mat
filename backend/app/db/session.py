# backend/app/db/session.py

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from app.core.config import settings

# ------------------------------------------------------------
# Database engine
# ------------------------------------------------------------

connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    future=True,
)

# ------------------------------------------------------------
# SQLite foreign key enforcement
# ------------------------------------------------------------

if settings.DATABASE_URL.startswith("sqlite"):

    @event.listens_for(Engine, "connect")
    def _enable_fk_constraints(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# ------------------------------------------------------------
# Session factory (NO scoped_session)
# ------------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)

# ------------------------------------------------------------
# FastAPI dependency
# One session per request, safely closed
# ------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

