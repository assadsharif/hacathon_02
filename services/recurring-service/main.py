"""
[Task]: T045-T047
Recurring Service - Auto-create next task instance when recurring task completed

Phase V: Event-Driven Architecture
Reference: specs/005-phase-v-event-driven/spec.md

Responsibilities:
- Listen for task.completed events for recurring tasks
- Calculate next occurrence based on recurrence rule
- Create next task instance via Dapr service invocation
"""

import os
import httpx
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel
from dateutil.relativedelta import relativedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
BACKEND_APP_ID = "backend"

app = FastAPI(
    title="Recurring Service",
    description="Phase V - Recurring Task Generator",
    version="1.0.0"
)


class RecurrenceConfig(BaseModel):
    """Recurrence configuration."""
    rule: str  # daily, weekly, monthly
    interval: int = 1


# ==================== Health Endpoints ====================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "recurring-service"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "recurring-service",
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

@app.post("/events/task-completed")
async def handle_task_completed(request: Request) -> Response:
    """
    [Task]: T045 - Handle task.completed event for recurring tasks

    When a recurring task is completed, automatically create the next instance.
    """
    try:
        body = await request.json()
        logger.info(f"Received task.completed event: {body.get('id')}")

        event_data = body.get("data", {})
        task_id = event_data.get("taskId")
        user_id = event_data.get("userId")
        is_recurring = event_data.get("isRecurring", False)
        recurrence = event_data.get("recurrence")

        if is_recurring and recurrence:
            rule = recurrence.get("rule")
            interval = recurrence.get("interval", 1)

            if rule:
                await create_next_occurrence(task_id, user_id, rule, interval)

        return Response(status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error handling task.completed: {e}")
        return Response(status_code=status.HTTP_200_OK)


# ==================== Helper Functions ====================

def calculate_next_occurrence(
    rule: str,
    interval: int,
    base_date: Optional[datetime] = None
) -> datetime:
    """
    [Task]: T046 - Calculate next occurrence based on recurrence rule

    Args:
        rule: Recurrence rule (daily, weekly, monthly)
        interval: Number of periods between occurrences
        base_date: Base date to calculate from (default: now)

    Returns:
        Next occurrence datetime
    """
    base = base_date or datetime.utcnow()

    if rule == "daily":
        return base + timedelta(days=interval)
    elif rule == "weekly":
        return base + timedelta(weeks=interval)
    elif rule == "monthly":
        return base + relativedelta(months=interval)
    else:
        # Default to daily if unknown rule
        logger.warning(f"Unknown recurrence rule: {rule}, defaulting to daily")
        return base + timedelta(days=interval)


async def create_next_occurrence(
    original_task_id: int,
    user_id: str,
    rule: str,
    interval: int
) -> bool:
    """
    [Task]: T047 - Create next task instance via Dapr service invocation

    Args:
        original_task_id: Original recurring task ID
        user_id: User ID
        rule: Recurrence rule
        interval: Recurrence interval

    Returns:
        True if created successfully
    """
    # First, get the original task details
    original_task = await get_task_details(original_task_id, user_id)

    if not original_task:
        logger.error(f"Could not fetch original task {original_task_id}")
        return False

    # Calculate next due date
    current_due = None
    if original_task.get("due_date"):
        try:
            current_due = datetime.fromisoformat(
                original_task["due_date"].replace("Z", "+00:00")
            )
        except (ValueError, TypeError):
            pass

    next_due = calculate_next_occurrence(rule, interval, current_due)

    # Calculate reminder if original had one
    next_reminder = None
    if original_task.get("reminder_at") and current_due:
        try:
            original_reminder = datetime.fromisoformat(
                original_task["reminder_at"].replace("Z", "+00:00")
            )
            # Maintain same offset from due date
            reminder_offset = current_due - original_reminder
            next_reminder = next_due - reminder_offset
        except (ValueError, TypeError):
            pass

    # Prepare new task data
    new_task = {
        "title": original_task.get("title", "Recurring Task"),
        "description": original_task.get("description"),
        "priority": original_task.get("priority", "medium"),
        "due_date": next_due.isoformat() + "Z",
        "recurrence": {
            "rule": rule,
            "interval": interval,
            "end_date": original_task.get("recurrence", {}).get("end_date")
        },
        "tags": original_task.get("tags", [])
    }

    if next_reminder:
        new_task["reminder_at"] = next_reminder.isoformat() + "Z"

    # Check if we've passed the recurrence end date
    recurrence_end = original_task.get("recurrence", {}).get("end_date")
    if recurrence_end:
        try:
            end_date = datetime.fromisoformat(recurrence_end.replace("Z", "+00:00"))
            if next_due > end_date:
                logger.info(
                    f"Recurrence ended for task {original_task_id} "
                    f"(end date: {recurrence_end})"
                )
                return True  # Success, but no new task created
        except (ValueError, TypeError):
            pass

    # Create new task via Dapr service invocation
    return await create_task_via_dapr(new_task, user_id)


async def get_task_details(task_id: int, user_id: str) -> Optional[Dict[str, Any]]:
    """Fetch task details via Dapr service invocation."""
    url = f"{DAPR_BASE_URL}/v1.0/invoke/{BACKEND_APP_ID}/method/api/todos/{task_id}"

    try:
        async with httpx.AsyncClient() as client:
            # Note: We need to pass auth token in real scenario
            # For now, using internal service-to-service call
            response = await client.get(url, timeout=10.0)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get task: {response.status_code}")
                return None

    except Exception as e:
        logger.error(f"Error fetching task details: {e}")
        return None


async def create_task_via_dapr(task_data: Dict[str, Any], user_id: str) -> bool:
    """
    Create a new task via Dapr service invocation to backend.

    Note: In production, this would need proper service-to-service auth.
    """
    url = f"{DAPR_BASE_URL}/v1.0/invoke/{BACKEND_APP_ID}/method/api/todos"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=task_data,
                headers={
                    "Content-Type": "application/json",
                    # In production: pass service account token
                    "X-User-Id": user_id  # Temporary: pass user context
                },
                timeout=10.0
            )

            if response.status_code in (200, 201):
                new_task = response.json()
                logger.info(
                    f"Created next recurring task: {new_task.get('id')} "
                    f"(due: {task_data.get('due_date')})"
                )
                return True
            else:
                logger.error(
                    f"Failed to create recurring task: "
                    f"{response.status_code} - {response.text}"
                )
                return False

    except Exception as e:
        logger.error(f"Error creating recurring task: {e}")
        return False


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
