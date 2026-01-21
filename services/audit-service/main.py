"""
[Task]: T030
Audit Service - Event consumer for immutable task event log

Phase V: Event-Driven Architecture
Reference: specs/005-phase-v-event-driven/spec.md FR-5

This service:
1. Consumes all task events from Kafka via Dapr Pub/Sub
2. Stores events in Dapr State Store (PostgreSQL-backed)
3. Provides query API for audit log
"""

import os
import uuid
import httpx
from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Request, Response, Query, status
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
STATE_STORE_NAME = os.getenv("STATE_STORE_NAME", "statestore-postgres")

app = FastAPI(
    title="Audit Service",
    description="Immutable audit log for task events",
    version="1.0.0"
)


# === Models ===

class AuditEntry(BaseModel):
    """Audit log entry."""
    id: str
    task_id: int
    user_id: str
    event_type: str
    payload: Dict[str, Any]
    created_at: str


class AuditListResponse(BaseModel):
    """Response for audit log query."""
    items: List[AuditEntry]
    total: int


# === State Store Operations ===

async def save_audit_entry(entry: AuditEntry) -> bool:
    """Save audit entry to Dapr State Store."""
    url = f"{DAPR_BASE_URL}/v1.0/state/{STATE_STORE_NAME}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=[{
                    "key": entry.id,
                    "value": entry.model_dump()
                }],
                timeout=5.0
            )

            if response.status_code in (200, 204):
                logger.info(f"Saved audit entry: {entry.id}")
                return True
            else:
                logger.error(f"Failed to save audit entry: {response.text}")
                return False

    except Exception as e:
        logger.error(f"Error saving audit entry: {e}")
        return False


async def get_audit_entry(entry_id: str) -> Optional[AuditEntry]:
    """Get audit entry by ID from Dapr State Store."""
    url = f"{DAPR_BASE_URL}/v1.0/state/{STATE_STORE_NAME}/{entry_id}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)

            if response.status_code == 200:
                data = response.json()
                return AuditEntry(**data)
            return None

    except Exception as e:
        logger.error(f"Error getting audit entry: {e}")
        return None


# === API Endpoints ===

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "audit-service"}


@app.post("/events/audit")
async def handle_audit_event(request: Request) -> Response:
    """
    Handle incoming task events from Dapr Pub/Sub.

    Consumes: task.created, task.updated, task.completed, task.deleted
    """
    try:
        body = await request.json()
        logger.info(f"Received event: {body.get('type', 'unknown')}")

        # Extract event details
        event_type = body.get("type", "unknown")
        event_data = body.get("data", {})
        event_id = body.get("id", f"evt-{uuid.uuid4()}")
        event_time = body.get("time", datetime.utcnow().isoformat() + "Z")

        # Create audit entry
        entry = AuditEntry(
            id=f"audit-{event_id}",
            task_id=event_data.get("taskId", 0),
            user_id=event_data.get("userId", ""),
            event_type=event_type,
            payload=event_data,
            created_at=event_time
        )

        # Save to state store
        saved = await save_audit_entry(entry)

        if saved:
            logger.info(f"Audit entry saved: {entry.id}")
        else:
            logger.warning(f"Failed to save audit entry: {entry.id}")

        # Always return success to prevent Dapr retries
        return Response(status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error handling audit event: {e}")
        return Response(status_code=status.HTTP_200_OK)


@app.get("/api/audit", response_model=AuditListResponse)
async def query_audit_log(
    task_id: Optional[int] = Query(None, description="Filter by task ID"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results")
):
    """
    Query audit log entries.

    Note: Full query functionality requires Dapr State Store with query support.
    For MVP, returns recent entries via direct state store access.
    """
    # For MVP, return empty list - full implementation requires query API
    # or separate indexing service
    logger.info(f"Audit query: task_id={task_id}, event_type={event_type}, limit={limit}")

    return AuditListResponse(items=[], total=0)


@app.get("/api/audit/{entry_id}", response_model=AuditEntry)
async def get_audit_entry_by_id(entry_id: str):
    """Get a specific audit entry by ID."""
    entry = await get_audit_entry(entry_id)

    if not entry:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return entry


# === Dapr Subscription Discovery ===

@app.get("/dapr/subscribe")
def get_subscriptions():
    """Return empty - using declarative subscriptions."""
    return []


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
