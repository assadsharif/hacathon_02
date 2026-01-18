"""
Database Configuration and Connection Management

This module handles the database connection to Neon PostgreSQL
and provides session management for database operations.
"""

from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
import os
from dotenv import load_dotenv
from sqlalchemy import text

# Load environment variables from .env file
load_dotenv()

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable not set. "
        "Please configure your Neon database connection string in .env file."
    )

# Create database engine with connection pooling
# Configuration optimized for Neon PostgreSQL serverless
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL statements (set to False in production)
    pool_size=5,  # Number of persistent connections to maintain
    max_overflow=10,  # Additional connections when pool is full
    pool_timeout=30,  # Wait time for connection (seconds)
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Verify connections before using
)


def create_db_and_tables():
    """
    Create all database tables defined in SQLModel models.

    This function should be called on application startup to ensure
    all tables exist in the database.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency function to get a database session.

    Usage in FastAPI endpoints:
        @app.get("/todos")
        def list_todos(session: Session = Depends(get_session)):
            # Use session to query database
            pass

    Yields:
        Session: SQLModel database session

    Example:
        with get_session() as session:
            todos = session.exec(select(Todo)).all()
    """
    with Session(engine) as session:
        yield session


def check_database_connection() -> bool:
    """
    Test database connectivity.

    Returns:
        bool: True if database is accessible, False otherwise

    Example:
        if check_database_connection():
            print("✅ Database connected")
        else:
            print("❌ Database connection failed")
    """
    try:
        with Session(engine) as session:
            # Execute a simple query to test connection
            session.exec(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
