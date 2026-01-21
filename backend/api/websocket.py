"""
[Task]: T050
WebSocket API - Real-time task updates

Phase V: Event-Driven Architecture
Provides WebSocket endpoint for clients to receive real-time task updates.
"""

import json
import logging
from typing import Dict, Set
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from starlette.websockets import WebSocketState
from jose import jwt
from jose.exceptions import JWTError

from auth import JWT_SECRET, ALGORITHM

logger = logging.getLogger(__name__)

router = APIRouter(tags=["WebSocket"])


class ConnectionManager:
    """
    [Task]: T051 - Manages WebSocket connections per user

    Tracks active WebSocket connections and provides broadcast capabilities.
    """

    def __init__(self):
        # Map of user_id -> set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and track a new WebSocket connection."""
        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()

        self.active_connections[user_id].add(websocket)
        logger.info(f"WebSocket connected for user {user_id}")

    def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove a WebSocket connection."""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"WebSocket disconnected for user {user_id}")

    async def broadcast_to_user(self, user_id: str, message: dict):
        """Send a message to all connections for a specific user."""
        if user_id not in self.active_connections:
            return

        dead_connections = set()

        for websocket in self.active_connections[user_id]:
            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send to WebSocket: {e}")
                dead_connections.add(websocket)

        # Clean up dead connections
        for ws in dead_connections:
            self.active_connections[user_id].discard(ws)

    async def broadcast_event(self, user_id: str, event_type: str, data: dict):
        """Broadcast an event to all connections for a user."""
        message = {
            "type": event_type,
            "data": data
        }
        await self.broadcast_to_user(user_id, message)

    def get_connection_count(self, user_id: str = None) -> int:
        """Get number of active connections."""
        if user_id:
            return len(self.active_connections.get(user_id, set()))
        return sum(len(conns) for conns in self.active_connections.values())


# Global connection manager instance
manager = ConnectionManager()


def get_user_from_token(token: str) -> str:
    """Extract user_id from JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id:
            return user_id
    except JWTError as e:
        logger.warning(f"Invalid JWT token: {e}")
    return None


@router.websocket("/ws/tasks")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    """
    [Task]: T050 - WebSocket endpoint for real-time task updates

    Clients connect with their JWT token to receive events:
    - task.created: New task created
    - task.updated: Task modified
    - task.completed: Task marked complete
    - task.deleted: Task removed
    - reminder.triggered: Reminder fired

    Usage:
        ws://localhost:8000/ws/tasks?token=<jwt_token>
    """
    # Authenticate user from token
    user_id = get_user_from_token(token)

    if not user_id:
        await websocket.close(code=4001, reason="Invalid or missing token")
        return

    await manager.connect(websocket, user_id)

    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connection.established",
            "data": {"user_id": user_id}
        })

        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Receive and handle messages (ping/pong, commands)
                data = await websocket.receive_text()
                message = json.loads(data)

                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})

            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                continue

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket, user_id)


# ==================== Event Integration ====================

async def broadcast_task_event(user_id: str, event: dict):
    """
    [Task]: T052 - Broadcast task event to WebSocket clients

    Called by events.py when receiving Dapr events.
    """
    await manager.broadcast_event(user_id, event.get("type"), event.get("data"))


# Export for use in events.py
def get_connection_manager() -> ConnectionManager:
    """Get the global connection manager."""
    return manager
