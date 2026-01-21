"""
[Task]: T018
Tag Schemas - Pydantic models for tag API requests/responses

Phase V: Event-Driven Architecture
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class TagBase(BaseModel):
    """Base schema for tag data."""
    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    """Schema for creating a tag."""
    pass


class TagResponse(TagBase):
    """Schema for tag response."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TagListResponse(BaseModel):
    """Schema for list of tags response."""
    items: List[TagResponse]
    total: int
