# app/database/database.py

from sqlmodel import SQLModel, create_engine, Session
import os

# Read from .env (local) or environment variables (VM)
DATABASE_URL = os.getenv("DATABASE_URL")

# If no database URL is found → default to SQLite for local testing
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./local.db"

# SQLite requires special connection arguments
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=True,           # Show SQL logs for debugging
    connect_args=connect_args
)

def init_db():
    """Create tables based on SQLModel metadata."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Provide a database session via dependency injection."""
    with Session(engine) as session:
        yield session
