"""
[Task]: T016
Tags API - REST endpoints for tag management

Phase V: Event-Driven Architecture
Reference: specs/005-phase-v-event-driven/contracts/api-extensions.yaml
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from database import get_session
from auth import get_current_user_id
from services.tag_service import TagService
from models.tag import Tag


# === Pydantic Schemas ===

class TagCreate(BaseModel):
    """Request schema for creating a tag."""
    name: str = Field(..., min_length=1, max_length=50, description="Tag name")

    class Config:
        json_schema_extra = {"example": {"name": "work"}}


class TagResponse(BaseModel):
    """Response schema for a tag."""
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "work",
                "created_at": "2026-01-20T12:00:00Z"
            }
        }


class TagListResponse(BaseModel):
    """Response schema for list of tags."""
    items: List[TagResponse]
    total: int


# === Router ===

router = APIRouter(prefix="/api/tags", tags=["Tags"])


@router.get("", response_model=TagListResponse)
def list_tags(
    session: Session = Depends(get_session),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    List all tags for the current user.

    Returns:
        List of user's tags sorted alphabetically
    """
    service = TagService(session)
    tags = service.list_tags(user_id)

    return TagListResponse(
        items=[TagResponse.model_validate(tag) for tag in tags],
        total=len(tags)
    )


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    data: TagCreate,
    session: Session = Depends(get_session),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Create a new tag.

    Args:
        data: Tag name

    Returns:
        Created tag

    Raises:
        400: Tag with same name already exists
    """
    service = TagService(session)

    try:
        tag = service.create_tag(data.name, user_id)
        return TagResponse.model_validate(tag)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(
    tag_id: int,
    session: Session = Depends(get_session),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Get a tag by ID.

    Args:
        tag_id: Tag ID

    Returns:
        Tag details

    Raises:
        404: Tag not found
    """
    service = TagService(session)
    tag = service.get_tag_by_id(tag_id, user_id)

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )

    return TagResponse.model_validate(tag)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    session: Session = Depends(get_session),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Delete a tag by ID.

    This will also remove the tag from all associated todos.

    Args:
        tag_id: Tag ID

    Raises:
        404: Tag not found
    """
    service = TagService(session)

    if not service.delete_tag(tag_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
