"""
Infrastructure — Supabase / SQLite Database Client
===================================================
SQLAlchemy engine, session ve Base.
Supabase PostgreSQL bağlantısı varsa kullanır,
yoksa SQLite'a fallback yapar.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

# Supabase varsa PostgreSQL, yoksa SQLite
DATABASE_URL = os.getenv("SUPABASE_DB_URL") or "sqlite:///./dus.db"

# SQLite için check_same_thread
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """SQLAlchemy ORM taban sınıfı."""
    pass


def get_db():
    """FastAPI dependency injection — DB session generator."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Tüm tabloları oluşturur."""
    Base.metadata.create_all(bind=engine)
