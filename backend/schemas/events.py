"""
[Task]: T022
Event Schemas - CloudEvents models for task lifecycle events

Phase V: Event-Driven Architecture
Reference: specs/005-phase-v-event-driven/contracts/event-schema.json
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Literal
from datetime import datetime


class RecurrenceData(BaseModel):
    """Recurrence configuration in event data."""
    rule: Literal["daily", "weekly", "monthly"]
    interval: int = 1
    endDate: Optional[int] = None  # Unix timestamp


class TaskCreatedData(BaseModel):
    """Data payload for task.created event."""
    taskId: int
    userId: str
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    dueDate: Optional[int] = None  # Unix timestamp
    reminderAt: Optional[int] = None  # Unix timestamp
    recurrence: Optional[RecurrenceData] = None
    tags: List[str] = []
    parentTaskId: Optional[int] = None
    createdAt: int  # Unix timestamp


class FieldChange(BaseModel):
    """Represents a changed field with old and new values."""
    old: Any
    new: Any


class TaskUpdatedData(BaseModel):
    """Data payload for task.updated event."""
    taskId: int
    userId: str
    changes: Dict[str, FieldChange]
    updatedAt: int  # Unix timestamp


class TaskCompletedData(BaseModel):
    """Data payload for task.completed event."""
    taskId: int
    userId: str
    isRecurring: bool = False
    recurrence: Optional[RecurrenceData] = None
    completedAt: int  # Unix timestamp


class TaskDeletedData(BaseModel):
    """Data payload for task.deleted event."""
    taskId: int
    userId: str
    deletedAt: int  # Unix timestamp


class CloudEventBase(BaseModel):
    """Base CloudEvents 1.0 structure."""
    specversion: str = "1.0"
    type: str
    source: str = "/todo-chatbot/backend"
    id: str
    time: str
    datacontenttype: str = "application/json"


class TaskCreatedEvent(CloudEventBase):
    """CloudEvent for task.created."""
    type: Literal["task.created"] = "task.created"
    data: TaskCreatedData


class TaskUpdatedEvent(CloudEventBase):
    """CloudEvent for task.updated."""
    type: Literal["task.updated"] = "task.updated"
    data: TaskUpdatedData


class TaskCompletedEvent(CloudEventBase):
    """CloudEvent for task.completed."""
    type: Literal["task.completed"] = "task.completed"
    data: TaskCompletedData


class TaskDeletedEvent(CloudEventBase):
    """CloudEvent for task.deleted."""
    type: Literal["task.deleted"] = "task.deleted"
    data: TaskDeletedData


# Union type for any task event
TaskEvent = TaskCreatedEvent | TaskUpdatedEvent | TaskCompletedEvent | TaskDeletedEvent
