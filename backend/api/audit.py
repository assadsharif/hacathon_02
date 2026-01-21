"""
[Task]: T034
Audit API - Query audit log via Dapr service invocation

Phase V: Event-Driven Architecture
Reference: specs/005-phase-v-event-driven/spec.md
"""

import os
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import uuid
import logging

from auth import get_current_user_id

logger = logging.getLogger(__name__)

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
AUDIT_SERVICE_APP_ID = "audit-service"

router = APIRouter(
    prefix="/api/audit",
    tags=["Audit"],
    responses={
        503: {"description": "Audit service unavailable"}
    }
)


class AuditEventResponse(BaseModel):
    """Response schema for audit events."""
    event_id: str
    event_type: str
    task_id: int
    user_id: str
    timestamp: datetime
    data: dict


class AuditListResponse(BaseModel):
    """Response schema for audit event list."""
    events: List[AuditEventResponse]
    total: int
    has_more: bool


@router.get("/", response_model=AuditListResponse)
async def get_audit_log(
    user_id: uuid.UUID = Depends(get_current_user_id),
    task_id: Optional[int] = Query(default=None, description="Filter by task ID"),
    event_type: Optional[str] = Query(
        default=None,
        description="Filter by event type (task.created, task.updated, task.completed, task.deleted)"
    ),
    since: Optional[datetime] = Query(default=None, description="Events since this timestamp"),
    limit: int = Query(default=50, ge=1, le=200, description="Max events to return")
):
    """
    Query audit log for the authenticated user.

    [Task]: T034 - Query audit log via Dapr service invocation

    This endpoint queries the audit-service via Dapr service invocation
    to retrieve immutable audit records of all task operations.

    Args:
        user_id: Authenticated user ID (from JWT)
        task_id: Optional filter by specific task
        event_type: Optional filter by event type
        since: Optional filter for events after this time
        limit: Maximum number of events to return

    Returns:
        AuditListResponse: List of audit events

    Raises:
        HTTPException 503: If audit service is unavailable
    """
    # Build query parameters
    params = {
        "user_id": str(user_id),
        "limit": limit
    }
    if task_id:
        params["task_id"] = task_id
    if event_type:
        params["event_type"] = event_type
    if since:
        params["since"] = since.isoformat()

    # Query audit service via Dapr service invocation
    url = f"{DAPR_BASE_URL}/v1.0/invoke/{AUDIT_SERVICE_APP_ID}/method/api/events"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)

            if response.status_code == 200:
                data = response.json()
                return AuditListResponse(
                    events=[AuditEventResponse(**event) for event in data.get("events", [])],
                    total=data.get("total", 0),
                    has_more=data.get("has_more", False)
                )
            else:
                logger.error(f"Audit service returned {response.status_code}: {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Audit service returned an error"
                )

    except httpx.ConnectError:
        logger.warning("Cannot connect to audit service via Dapr")
        # Return empty result when audit service is unavailable (graceful degradation)
        return AuditListResponse(events=[], total=0, has_more=False)

    except httpx.TimeoutException:
        logger.warning("Timeout connecting to audit service")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Audit service timed out"
        )


@router.get("/task/{task_id}", response_model=AuditListResponse)
async def get_task_audit_history(
    task_id: int,
    user_id: uuid.UUID = Depends(get_current_user_id),
    limit: int = Query(default=50, ge=1, le=200, description="Max events to return")
):
    """
    Get complete audit history for a specific task.

    Args:
        task_id: Task ID to get history for
        user_id: Authenticated user ID (from JWT)
        limit: Maximum number of events to return

    Returns:
        AuditListResponse: List of audit events for the task
    """
    return await get_audit_log(
        user_id=user_id,
        task_id=task_id,
        event_type=None,
        since=None,
        limit=limit
    )
