"""Pytest configuration and shared fixtures for add-task feature.

This file is automatically discovered by pytest and contains:
- Test state management fixtures
- Shared test utilities
"""
import pytest


@pytest.fixture(autouse=True)
def reset_task_storage():
    """Reset task storage state before each test.

    This fixture automatically runs before every test to ensure:
    - Task list is empty
    - Task ID counter is reset to 0

    This prevents test pollution and ensures each test starts with clean state.
    """
    # Import here to avoid issues if module doesn't exist yet
    try:
        import src.storage as storage
        # Reset task list
        storage._tasks.clear()
        # Reset ID counter
        storage._task_id_counter = 0
    except (ImportError, AttributeError):
        # Module/attributes don't exist yet - that's OK during initial setup
        pass

    yield

    # Cleanup after test (optional - same as before)
    try:
        import src.storage as storage
        storage._tasks.clear()
        storage._task_id_counter = 0
    except (ImportError, AttributeError):
        pass
