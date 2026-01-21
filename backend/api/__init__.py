"""
[Task]: T016, T027, T034, T050
API Package - Phase V routers

Exports:
    - tags_router: Tag management endpoints
    - events_router: Dapr event subscription callbacks
    - audit_router: Audit log query endpoints
    - websocket_router: Real-time WebSocket endpoint
"""

from api.tags import router as tags_router
from api.events import router as events_router
from api.audit import router as audit_router
from api.websocket import router as websocket_router

__all__ = ["tags_router", "events_router", "audit_router", "websocket_router"]
