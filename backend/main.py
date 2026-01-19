"""
FastAPI Backend - Phase II Todo Application

This is the main entry point for the FastAPI backend server.
It provides RESTful API endpoints for the Phase II web application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Startup: Create database tables
    Shutdown: Cleanup resources
    """
    # Import models to register them with SQLModel
    # [Task]: AUTH-A1 - Register User model for table creation
    from models import Todo, User  # noqa: F401
    from database import create_db_and_tables

    print("🚀 Starting FastAPI server...")
    print("📊 Creating database tables...")
    create_db_and_tables()
    print("✅ Database tables created successfully")

    yield

    # Shutdown: Cleanup if needed
    print("👋 Shutting down FastAPI server...")


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Phase II - Full-Stack Todo Application API",
    lifespan=lifespan
)

# CORS middleware configuration
# Allow Next.js frontend (http://localhost:3000) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",  # Alternative localhost
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    API root endpoint.
    Returns basic information about the API.
    """
    return {
        "message": "Todo API - Phase II",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns the health status of the API.
    """
    return {
        "status": "healthy",
        "service": "todo-api",
        "version": "1.0.0"
    }


# Database health check endpoint
@app.get("/health/db", tags=["Health"])
async def database_health_check():
    """
    Database health check endpoint.
    Verifies database connectivity.
    """
    from database import check_database_connection

    is_connected = check_database_connection()

    if is_connected:
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Database connection successful"
        }
    else:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "message": "Database connection failed"
        }


# Include routers
from routers import todos
from routers import auth_router

app.include_router(todos.router)
app.include_router(auth_router.router)
