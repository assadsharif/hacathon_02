"""
[Task]: T037-T040
Reminder Service - Schedule and manage task reminders via Dapr Jobs API

Phase V: Event-Driven Architecture
Reference: specs/005-phase-v-event-driven/spec.md

Responsibilities:
- Listen for task.created events to schedule reminders
- Listen for task.updated events to reschedule/cancel reminders
- Listen for task.deleted events to cancel reminders
- Handle job callbacks when reminders fire
"""

import os
import httpx
import logging
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
BACKEND_APP_ID = "backend"
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "pubsub-kafka")

app = FastAPI(
    title="Reminder Service",
    description="Phase V - Task Reminder Scheduler via Dapr Jobs API",
    version="1.0.0"
)


class CloudEvent(BaseModel):
    """Incoming CloudEvent from Dapr Pub/Sub."""
    specversion: str = "1.0"
    type: str
    source: str
    id: str
    time: str
    datacontenttype: str = "application/json"
    data: Dict[str, Any]


class ReminderJobData(BaseModel):
    """Data stored with reminder job."""
    task_id: int
    user_id: str
    title: str
    reminder_at: int  # Unix timestamp


# ==================== Health Endpoints ====================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "reminder-service"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "reminder-service",
        "version": "1.0.0",
        "phase": "V"
    }


# ==================== Dapr Subscription Discovery ====================

@app.get("/dapr/subscribe")
async def get_subscriptions():
    """
    Dapr subscription discovery endpoint.
    Returns empty - using declarative subscriptions via YAML.
    """
    return []


# ==================== Event Handlers ====================

@app.post("/events/task-created")
async def handle_task_created(request: Request) -> Response:
    """
    [Task]: T037 - Handle task.created event

    Schedule a reminder if the task has reminder_at set.
    """
    try:
        body = await request.json()
        logger.info(f"Received task.created event: {body.get('id')}")

        event_data = body.get("data", {})
        task_id = event_data.get("taskId")
        user_id = event_data.get("userId")
        title = event_data.get("title")
        reminder_at = event_data.get("reminderAt")  # Unix timestamp

        if reminder_at and task_id and user_id:
            await schedule_reminder(task_id, user_id, title, reminder_at)

        return Response(status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error handling task.created: {e}")
        return Response(status_code=status.HTTP_200_OK)


@app.post("/events/task-updated")
async def handle_task_updated(request: Request) -> Response:
    """
    [Task]: T039 - Handle task.updated event

    Reschedule or cancel reminder if reminder_at changed.
    """
    try:
        body = await request.json()
        logger.info(f"Received task.updated event: {body.get('id')}")

        event_data = body.get("data", {})
        task_id = event_data.get("taskId")
        user_id = event_data.get("userId")
        changes = event_data.get("changes", {})

        # Check if reminder_at was changed
        if "reminder_at" in changes or "reminderAt" in changes:
            reminder_change = changes.get("reminder_at") or changes.get("reminderAt", {})
            new_reminder = reminder_change.get("new")

            # Cancel existing reminder
            await cancel_reminder(task_id)

            # Schedule new reminder if set
            if new_reminder:
                # Fetch task title via Dapr service invocation
                title = await get_task_title(task_id, user_id)
                await schedule_reminder(task_id, user_id, title, new_reminder)

        return Response(status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error handling task.updated: {e}")
        return Response(status_code=status.HTTP_200_OK)


@app.post("/events/task-deleted")
async def handle_task_deleted(request: Request) -> Response:
    """
    [Task]: T039 - Handle task.deleted event

    Cancel any scheduled reminder for the deleted task.
    """
    try:
        body = await request.json()
        logger.info(f"Received task.deleted event: {body.get('id')}")

        event_data = body.get("data", {})
        task_id = event_data.get("taskId")

        if task_id:
            await cancel_reminder(task_id)

        return Response(status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error handling task.deleted: {e}")
        return Response(status_code=status.HTTP_200_OK)


@app.post("/events/task-completed")
async def handle_task_completed(request: Request) -> Response:
    """
    Handle task.completed event - cancel any scheduled reminder.
    """
    try:
        body = await request.json()
        logger.info(f"Received task.completed event: {body.get('id')}")

        event_data = body.get("data", {})
        task_id = event_data.get("taskId")

        if task_id:
            await cancel_reminder(task_id)

        return Response(status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error handling task.completed: {e}")
        return Response(status_code=status.HTTP_200_OK)


# ==================== Job Callback Handler ====================

@app.post("/job/{job_name}")
async def handle_job_callback(job_name: str, request: Request) -> Response:
    """
    [Task]: T040 - Handle triggered reminder job callback

    When a reminder job fires, this endpoint is called by Dapr Jobs API.
    We publish a reminder.triggered event that the frontend can consume.
    """
    try:
        body = await request.json()
        logger.info(f"Reminder job triggered: {job_name}")

        # Extract job data
        job_data = body.get("data", {})
        task_id = job_data.get("task_id")
        user_id = job_data.get("user_id")
        title = job_data.get("title", "Task Reminder")

        # Publish reminder.triggered event
        await publish_reminder_triggered(task_id, user_id, title)

        return Response(status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error handling job callback: {e}")
        return Response(status_code=status.HTTP_200_OK)


# ==================== Helper Functions ====================

async def schedule_reminder(
    task_id: int,
    user_id: str,
    title: str,
    reminder_at: int
) -> bool:
    """
    [Task]: T038 - Schedule a reminder using Dapr Jobs API

    Args:
        task_id: Task ID
        user_id: User ID
        title: Task title for notification
        reminder_at: Unix timestamp when to trigger reminder

    Returns:
        True if scheduled successfully
    """
    job_name = f"reminder-{task_id}"

    # Calculate delay from now
    now = datetime.utcnow().timestamp()
    delay_seconds = max(0, reminder_at - now)

    if delay_seconds <= 0:
        logger.info(f"Reminder time already passed for task {task_id}")
        return False

    # Dapr Jobs API endpoint
    url = f"{DAPR_BASE_URL}/v1.0-alpha1/jobs/{job_name}"

    job_data = {
        "data": {
            "task_id": task_id,
            "user_id": user_id,
            "title": title,
            "reminder_at": reminder_at
        },
        "schedule": f"@every {int(delay_seconds)}s",
        "repeats": 1,  # One-time job
        "dueTime": f"{int(delay_seconds)}s"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=job_data, timeout=5.0)

            if response.status_code in (200, 201, 204):
                logger.info(f"Scheduled reminder for task {task_id} in {delay_seconds}s")
                return True
            else:
                logger.error(f"Failed to schedule reminder: {response.status_code}")
                return False

    except httpx.ConnectError:
        logger.warning("Dapr sidecar not available for Jobs API")
        return False
    except Exception as e:
        logger.error(f"Error scheduling reminder: {e}")
        return False


async def cancel_reminder(task_id: int) -> bool:
    """
    [Task]: T039 - Cancel a scheduled reminder

    Args:
        task_id: Task ID

    Returns:
        True if cancelled successfully
    """
    job_name = f"reminder-{task_id}"
    url = f"{DAPR_BASE_URL}/v1.0-alpha1/jobs/{job_name}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, timeout=5.0)

            if response.status_code in (200, 204, 404):
                logger.info(f"Cancelled reminder for task {task_id}")
                return True
            else:
                logger.error(f"Failed to cancel reminder: {response.status_code}")
                return False

    except httpx.ConnectError:
        logger.warning("Dapr sidecar not available")
        return False
    except Exception as e:
        logger.error(f"Error cancelling reminder: {e}")
        return False


async def get_task_title(task_id: int, user_id: str) -> str:
    """Get task title via Dapr service invocation."""
    url = f"{DAPR_BASE_URL}/v1.0/invoke/{BACKEND_APP_ID}/method/api/todos/{task_id}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            if response.status_code == 200:
                return response.json().get("title", "Task Reminder")
    except Exception as e:
        logger.error(f"Error getting task title: {e}")

    return "Task Reminder"


async def publish_reminder_triggered(
    task_id: int,
    user_id: str,
    title: str
) -> bool:
    """Publish reminder.triggered event to notify user."""
    url = f"{DAPR_BASE_URL}/v1.0/publish/{PUBSUB_NAME}/reminder-events"

    event = {
        "specversion": "1.0",
        "type": "reminder.triggered",
        "source": "/todo-chatbot/reminder-service",
        "id": f"rem-{task_id}-{int(datetime.utcnow().timestamp())}",
        "time": datetime.utcnow().isoformat() + "Z",
        "datacontenttype": "application/json",
        "data": {
            "taskId": task_id,
            "userId": user_id,
            "title": title,
            "triggeredAt": int(datetime.utcnow().timestamp())
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=event,
                headers={"Content-Type": "application/cloudevents+json"},
                timeout=5.0
            )
            return response.status_code in (200, 204)
    except Exception as e:
        logger.error(f"Error publishing reminder event: {e}")
        return False


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
