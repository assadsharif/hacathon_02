"""
[Task]: T027, T052
Events API - Dapr subscription callback endpoints

Phase V: Event-Driven Architecture
Handles incoming events from Dapr Pub/Sub for WebSocket broadcast
"""

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Events"])


# Import WebSocket broadcast function
def get_broadcast_func():
    """Lazy import to avoid circular dependency."""
    try:
        from api.websocket import broadcast_task_event
        return broadcast_task_event
    except ImportError:
        return None


class DaprSubscription(BaseModel):
    """Dapr subscription configuration."""
    pubsubname: str
    topic: str
    route: str


class CloudEventRequest(BaseModel):
    """Incoming CloudEvent from Dapr."""
    specversion: str
    type: str
    source: str
    id: str
    time: str
    datacontenttype: str
    data: Dict[str, Any]


@router.get("/dapr/subscribe")
def get_subscriptions() -> List[DaprSubscription]:
    """
    Dapr subscription discovery endpoint.

    Dapr calls this endpoint to discover which topics this app subscribes to.
    Note: We use declarative subscriptions via YAML, so this returns empty.
    Keeping endpoint for debugging and potential programmatic subscriptions.
    """
    return []


@router.post("/task")
async def handle_task_event(request: Request) -> Response:
    """
    [Task]: T052 - Handle incoming task events from Dapr Pub/Sub.

    This endpoint receives all task lifecycle events and broadcasts
    them to connected WebSocket clients for real-time sync.

    Events: task.created, task.updated, task.completed, task.deleted
    """
    try:
        body = await request.json()
        logger.info(f"Received event: {body.get('type', 'unknown')}")

        event_type = body.get("type")
        event_data = body.get("data", {})

        # Broadcast to WebSocket clients
        broadcast_func = get_broadcast_func()
        if broadcast_func:
            user_id = event_data.get("userId")
            if user_id:
                await broadcast_func(user_id, {
                    "type": event_type,
                    "data": event_data
                })
                logger.info(f"Broadcast event to user {user_id}")

        # Return success to Dapr
        return Response(status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error handling event: {e}")
        # Return success to prevent Dapr retries for non-recoverable errors
        return Response(status_code=status.HTTP_200_OK)


@router.options("/task")
async def options_task_event():
    """Handle CORS preflight for task events endpoint."""
    return Response(status_code=status.HTTP_200_OK)
