"""
database.py — SQLite Database Connection & Session Management
VayuBus Backend
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ── DB URL ────────────────────────────────────────────────────
# SQLite for dev — change to PostgreSQL for production
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./vayubus.db"
)

# PostgreSQL example (set in k8s secret):
# DATABASE_URL = "postgresql://user:password@postgres-svc:5432/vayubus"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite only
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ── Dependency for FastAPI routes ─────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
