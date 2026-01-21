"""
[Task]: T021
Event Publisher - Dapr Pub/Sub client for publishing task events

Phase V: Event-Driven Architecture
Reference: specs/005-phase-v-event-driven/contracts/event-schema.json
"""

import os
import uuid
import httpx
from datetime import datetime
from typing import Any, Dict, Optional, List
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "pubsub-kafka")
TOPIC_NAME = os.getenv("TOPIC_NAME", "task-events")


class CloudEvent(BaseModel):
    """CloudEvents 1.0 envelope for task events."""
    specversion: str = "1.0"
    type: str
    source: str = "/todo-chatbot/backend"
    id: str
    time: str
    datacontenttype: str = "application/json"
    data: Dict[str, Any]


class EventPublisher:
    """
    Publisher for task lifecycle events via Dapr Pub/Sub.

    Publishes CloudEvents-formatted messages to Kafka topic.
    """

    def __init__(self):
        self.pubsub_name = PUBSUB_NAME
        self.topic_name = TOPIC_NAME
        self.base_url = DAPR_BASE_URL
        self._enabled = os.getenv("EVENTS_ENABLED", "true").lower() == "true"

    def _generate_event_id(self) -> str:
        """Generate unique event ID."""
        return f"evt-{uuid.uuid4()}"

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.utcnow().isoformat() + "Z"

    def _to_unix_timestamp(self, dt: Optional[datetime]) -> Optional[int]:
        """Convert datetime to Unix timestamp."""
        if dt is None:
            return None
        return int(dt.timestamp())

    async def _publish(self, event: CloudEvent, retries: int = 3) -> bool:
        """
        [Task]: T064, T065 - Publish event to Dapr Pub/Sub with retry logic.

        Args:
            event: CloudEvent to publish
            retries: Number of retry attempts for transient failures

        Returns:
            True if published successfully, False otherwise
        """
        if not self._enabled:
            logger.info(f"Events disabled, skipping: {event.type}")
            return True

        url = f"{self.base_url}/v1.0/publish/{self.pubsub_name}/{self.topic_name}"

        last_error = None
        for attempt in range(retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        url,
                        json=event.model_dump(),
                        headers={
                            "Content-Type": "application/cloudevents+json",
                        },
                        timeout=5.0
                    )

                    if response.status_code in (200, 204):
                        logger.info(f"Published event: {event.type} (id={event.id})")
                        return True
                    elif response.status_code >= 500:
                        # Server error - retry
                        last_error = f"Server error: {response.status_code}"
                        logger.warning(
                            f"Retry {attempt + 1}/{retries} for event {event.type}: {last_error}"
                        )
                        await self._exponential_backoff(attempt)
                        continue
                    else:
                        # Client error - don't retry
                        logger.error(
                            f"Failed to publish event: {response.status_code} - {response.text}"
                        )
                        return False

            except httpx.ConnectError as e:
                last_error = f"Connection error: {e}"
                if attempt < retries - 1:
                    logger.warning(
                        f"Retry {attempt + 1}/{retries} - Dapr sidecar connection failed"
                    )
                    await self._exponential_backoff(attempt)
                else:
                    logger.error(
                        f"Dapr sidecar not available after {retries} attempts: {event.type}"
                    )

            except httpx.TimeoutException as e:
                last_error = f"Timeout: {e}"
                if attempt < retries - 1:
                    logger.warning(
                        f"Retry {attempt + 1}/{retries} - Request timed out"
                    )
                    await self._exponential_backoff(attempt)
                else:
                    logger.error(f"Request timed out after {retries} attempts")

            except Exception as e:
                last_error = str(e)
                logger.error(f"Unexpected error publishing event: {e}")
                return False

        logger.error(f"Failed to publish event after {retries} attempts: {last_error}")
        return False

    async def _exponential_backoff(self, attempt: int) -> None:
        """[Task]: T065 - Exponential backoff for retries."""
        import asyncio
        delay = min(2 ** attempt * 0.5, 10)  # Max 10 seconds
        await asyncio.sleep(delay)

    async def publish_task_created(
        self,
        task_id: int,
        user_id: uuid.UUID,
        title: str,
        description: Optional[str],
        status: str,
        priority: str,
        due_date: Optional[datetime],
        reminder_at: Optional[datetime],
        recurrence_rule: Optional[str],
        recurrence_interval: int,
        recurrence_end_date: Optional[datetime],
        tags: List[str],
        created_at: datetime
    ) -> bool:
        """Publish task.created event."""
        event = CloudEvent(
            type="task.created",
            id=self._generate_event_id(),
            time=self._get_timestamp(),
            data={
                "taskId": task_id,
                "userId": str(user_id),
                "title": title,
                "description": description,
                "status": status,
                "priority": priority,
                "dueDate": self._to_unix_timestamp(due_date),
                "reminderAt": self._to_unix_timestamp(reminder_at),
                "recurrence": {
                    "rule": recurrence_rule,
                    "interval": recurrence_interval,
                    "endDate": self._to_unix_timestamp(recurrence_end_date)
                } if recurrence_rule else None,
                "tags": tags,
                "createdAt": self._to_unix_timestamp(created_at)
            }
        )
        return await self._publish(event)

    async def publish_task_updated(
        self,
        task_id: int,
        user_id: uuid.UUID,
        changes: Dict[str, Dict[str, Any]],
        updated_at: datetime
    ) -> bool:
        """
        Publish task.updated event.

        Args:
            task_id: Task ID
            user_id: User ID
            changes: Dictionary of changed fields with old/new values
            updated_at: Update timestamp
        """
        event = CloudEvent(
            type="task.updated",
            id=self._generate_event_id(),
            time=self._get_timestamp(),
            data={
                "taskId": task_id,
                "userId": str(user_id),
                "changes": changes,
                "updatedAt": self._to_unix_timestamp(updated_at)
            }
        )
        return await self._publish(event)

    async def publish_task_completed(
        self,
        task_id: int,
        user_id: uuid.UUID,
        is_recurring: bool,
        recurrence_rule: Optional[str],
        recurrence_interval: int,
        completed_at: datetime
    ) -> bool:
        """Publish task.completed event."""
        event = CloudEvent(
            type="task.completed",
            id=self._generate_event_id(),
            time=self._get_timestamp(),
            data={
                "taskId": task_id,
                "userId": str(user_id),
                "isRecurring": is_recurring,
                "recurrence": {
                    "rule": recurrence_rule,
                    "interval": recurrence_interval
                } if is_recurring else None,
                "completedAt": self._to_unix_timestamp(completed_at)
            }
        )
        return await self._publish(event)

    async def publish_task_deleted(
        self,
        task_id: int,
        user_id: uuid.UUID,
        deleted_at: datetime
    ) -> bool:
        """Publish task.deleted event."""
        event = CloudEvent(
            type="task.deleted",
            id=self._generate_event_id(),
            time=self._get_timestamp(),
            data={
                "taskId": task_id,
                "userId": str(user_id),
                "deletedAt": self._to_unix_timestamp(deleted_at)
            }
        )
        return await self._publish(event)


# Singleton instance
_publisher: Optional[EventPublisher] = None


def get_event_publisher() -> EventPublisher:
    """Get or create EventPublisher singleton."""
    global _publisher
    if _publisher is None:
        _publisher = EventPublisher()
    return _publisher
