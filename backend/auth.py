"""
[Task]: AUTH-B2
[From]: authentication.spec.md FR-AUTH-009, plan.md JWT Verification Middleware

Authentication and Authorization

This module provides JWT token verification for protecting API endpoints.
All protected routes use the get_current_user_id dependency to extract
and validate the authenticated user from the JWT token.

Security Model:
- JWT tokens issued by Better Auth (frontend)
- HS256 signing algorithm
- Tokens verified on every protected endpoint
- user_id extracted from token claims
- Invalid/expired tokens rejected with 401 Unauthorized
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jose import JWTError, jwt
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"  # HMAC-SHA256 (symmetric signing)

# Validate JWT_SECRET is configured
if not JWT_SECRET:
    raise ValueError(
        "JWT_SECRET environment variable not set. "
        "Please configure your JWT secret key in .env file."
    )

# HTTP Bearer token authentication scheme
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> uuid.UUID:
    """
    Extract and verify JWT token, return authenticated user_id.

    This dependency is used to protect API endpoints and enforce authentication.
    It extracts the JWT token from the Authorization header, verifies the
    signature, and returns the user_id from the token claims.

    Args:
        credentials: HTTPAuthorizationCredentials from Authorization header

    Returns:
        uuid.UUID: Authenticated user's UUID

    Raises:
        HTTPException 401: If token is invalid, expired, or malformed
        HTTPException 401: If token is missing user_id claim

    Usage:
        @router.get("/api/todos")
        async def list_todos(
            user_id: str = Depends(get_current_user_id),
            session: Session = Depends(get_session)
        ):
            # user_id is now available and authenticated
            todos = session.exec(
                select(Todo).where(Todo.user_id == user_id)
            ).all()
            return todos

    Security:
        - Verifies JWT signature using shared secret
        - Checks token expiration (exp claim)
        - Validates token structure
        - Extracts user_id from claims
    """
    try:
        # Extract token from Bearer scheme
        token = credentials.credentials

        # Decode and verify JWT
        # This will raise JWTError if:
        # - Signature is invalid
        # - Token is expired
        # - Token is malformed
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])

        # Extract user_id from token claims
        user_id_str: str = payload.get("user_id")

        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id claim",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Convert string UUID to UUID object
        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: malformed user_id",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except JWTError as e:
        # Token verification failed
        # Could be: invalid signature, expired, malformed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Optional: Helper function to create JWT tokens (for testing)
# In production, Better Auth creates tokens on the frontend
def create_access_token(user_id: str, email: str, expires_delta: int = 604800) -> str:
    """
    Create a JWT access token (for testing purposes).

    In production, Better Auth creates tokens on the frontend.
    This function is provided for testing and development.

    Args:
        user_id: User's UUID
        email: User's email address
        expires_delta: Token expiration in seconds (default: 7 days)

    Returns:
        str: Encoded JWT token

    Example:
        token = create_access_token(
            user_id="123e4567-e89b-12d3-a456-426614174000",
            email="user@example.com"
        )
    """
    from datetime import datetime, timedelta

    # Token payload
    payload = {
        "user_id": user_id,
        "email": email,
        "iat": datetime.utcnow(),  # Issued at
        "exp": datetime.utcnow() + timedelta(seconds=expires_delta),  # Expiration
    }

    # Encode and sign token
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return token
