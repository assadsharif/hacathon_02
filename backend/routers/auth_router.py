"""
Authentication Router

Provides user registration and login endpoints.
Bypasses Better Auth and handles authentication directly in the backend.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
import uuid
import bcrypt

from database import get_session
from models import User
from auth import create_access_token, get_current_user_id

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class SignUpRequest(BaseModel):
    """Request body for user registration"""
    name: str
    email: EmailStr
    password: str


class SignInRequest(BaseModel):
    """Request body for user login"""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Response for successful authentication"""
    user: dict
    token: str


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


@router.post("/sign-up", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(
    request: SignUpRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user.

    Creates a new user account and returns a JWT token.
    """
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == request.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Validate password length
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )

    # Create new user
    user_id = uuid.uuid4()
    password_hash = hash_password(request.password)

    new_user = User(
        id=user_id,
        name=request.name,
        email=request.email,
        password_hash=password_hash
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Generate JWT token
    token = create_access_token(user_id=str(user_id), email=request.email)

    return AuthResponse(
        user={
            "id": str(new_user.id),
            "name": new_user.name,
            "email": new_user.email
        },
        token=token
    )


@router.post("/sign-in", response_model=AuthResponse)
async def sign_in(
    request: SignInRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate a user.

    Verifies credentials and returns a JWT token.
    """
    # Find user by email
    user = session.exec(
        select(User).where(User.email == request.email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = create_access_token(user_id=str(user.id), email=user.email)

    return AuthResponse(
        user={
            "id": str(user.id),
            "name": user.name,
            "email": user.email
        },
        token=token
    )


@router.get("/me")
async def get_current_user_info(
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get the current authenticated user.

    Requires a valid JWT token.
    """
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email
    }
