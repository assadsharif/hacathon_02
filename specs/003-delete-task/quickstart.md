# Quickstart Guide: Implement Delete Task by ID

**Feature**: 003-delete-task | **Created**: 2026-01-13 | **For**: Developers implementing this feature

## Purpose

This quickstart guide provides step-by-step instructions for implementing the delete task feature using Test-Driven Development (TDD). Follow the RED-GREEN-REFACTOR cycle mandated by the project constitution.

## Prerequisites

Before starting implementation:

1. **Verify foundation is intact**:
   ```bash
   # Run existing tests to ensure 001-add-task and 002-mark-complete work
   pytest tests/ -v
   ```

   All tests from previous features must pass before proceeding.

2. **Confirm branch**:
   ```bash
   git branch
   # Should show: * 003-delete-task
   ```

3. **Review documentation**:
   - [spec.md](./spec.md) - Feature requirements
   - [plan.md](./plan.md) - Implementation approach
   - [research.md](./research.md) - Technical decisions
   - [data-model.md](./data-model.md) - Data structures and contracts

## TDD Workflow Overview

```
RED → GREEN → REFACTOR (repeat for each requirement)
```

1. **RED**: Write a failing test that defines desired behavior
2. **GREEN**: Write minimum code to make the test pass
3. **REFACTOR**: Clean up code while keeping tests passing

**CRITICAL**: Never skip the RED phase. Always verify tests fail before implementing.

## Implementation Steps

### Phase 1: Setup and Verification (If Needed)

**Goal**: Ensure test infrastructure is ready

#### Step 1.1: Verify Test File Exists

```bash
# Check if test file exists from previous features
ls tests/unit/test_task_manager.py
```

If file exists and contains tests for add_task and toggle_task_completion, proceed to Phase 2.

If file doesn't exist, create it:

```python
# tests/unit/test_task_manager.py
import pytest
from datetime import datetime
from src.task_manager import add_task, toggle_task_completion, delete_task
from src.storage import _tasks, reset_storage

@pytest.fixture(autouse=True)
def reset_test_storage():
    """Reset storage before each test"""
    reset_storage()
    yield
    reset_storage()
```

### Phase 2: Core Delete Functionality (User Story 1 - Priority P1)

**Goal**: Implement basic task deletion with confirmation

#### Step 2.1: RED - Test Task Deletion Removes from Storage

```python
# tests/unit/test_task_manager.py

def test_delete_task_removes_task_from_storage():
    """Test that delete_task removes the specified task from storage"""
    # Arrange: Create a task
    task = add_task("Task to delete", "This will be removed")
    task_id = task['id']

    # Act: Delete the task
    deleted = delete_task(task_id)

    # Assert: Task no longer in storage
    from src.storage import _tasks
    assert len(_tasks) == 0
    assert not any(t.id == task_id for t in _tasks)
```

**Run test (should FAIL)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_removes_task_from_storage -v
```

Expected error: `ImportError: cannot import name 'delete_task'` or `AttributeError: module has no attribute 'delete_task'`

#### Step 2.2: GREEN - Implement delete_task Function Stub

```python
# src/task_manager.py

from typing import Any
from src.storage import _tasks

def delete_task(task_id: int) -> dict[str, Any]:
    """Delete a task by its ID, removing it permanently from storage.

    Args:
        task_id: The ID of the task to delete

    Returns:
        Dictionary with all task fields before deletion

    Raises:
        ValueError: If task with given ID does not exist
    """
    # Find task by ID (linear search)
    task = None
    for t in _tasks:
        if t.id == task_id:
            task = t
            break

    # Handle task not found
    if task is None:
        print(f"✗ Error: Task #{task_id} not found")
        raise ValueError(f"Task #{task_id} not found")

    # Capture task data BEFORE deletion
    deleted_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }

    # Remove task from storage
    _tasks.remove(task)

    # Print confirmation message
    print(f"✓ Task #{task.id} deleted: {task.title}")

    # Return captured task data
    return deleted_data
```

**Run test (should PASS)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_removes_task_from_storage -v
```

#### Step 2.3: RED - Test Return Value Contains All Fields

```python
def test_delete_task_returns_all_task_fields():
    """Test that delete_task returns dictionary with all task fields"""
    # Arrange: Create a task with all fields populated
    task = add_task("Complete task", "With description")
    task_id = task['id']
    expected_title = "Complete task"
    expected_description = "With description"
    expected_completed = False

    # Act: Delete the task
    deleted = delete_task(task_id)

    # Assert: Return value contains all fields
    assert 'id' in deleted
    assert 'title' in deleted
    assert 'description' in deleted
    assert 'completed' in deleted
    assert 'created_at' in deleted

    assert deleted['id'] == task_id
    assert deleted['title'] == expected_title
    assert deleted['description'] == expected_description
    assert deleted['completed'] == expected_completed
    assert isinstance(deleted['created_at'], datetime)
```

**Run test (should PASS with current implementation)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_returns_all_task_fields -v
```

If test passes, no changes needed. If it fails, verify the implementation captures all fields.

#### Step 2.4: RED - Test Selective Deletion (Only Target Task Removed)

```python
def test_delete_task_only_removes_target_task():
    """Test that deleting one task does not affect other tasks"""
    # Arrange: Create multiple tasks
    task1 = add_task("Task 1", "First task")
    task2 = add_task("Task 2", "Second task")
    task3 = add_task("Task 3", "Third task")

    task1_id = task1['id']
    task2_id = task2['id']
    task3_id = task3['id']

    # Act: Delete the middle task
    delete_task(task2_id)

    # Assert: Tasks 1 and 3 still exist with unchanged data
    from src.storage import _tasks
    assert len(_tasks) == 2

    remaining_ids = [t.id for t in _tasks]
    assert task1_id in remaining_ids
    assert task2_id not in remaining_ids
    assert task3_id in remaining_ids

    # Verify task data unchanged
    task1_obj = next(t for t in _tasks if t.id == task1_id)
    assert task1_obj.title == "Task 1"
    assert task1_obj.description == "First task"

    task3_obj = next(t for t in _tasks if t.id == task3_id)
    assert task3_obj.title == "Task 3"
    assert task3_obj.description == "Third task"
```

**Run test (should PASS with current implementation)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_only_removes_target_task -v
```

#### Step 2.5: RED - Test Confirmation Message Output

```python
def test_delete_task_prints_confirmation_message(capsys):
    """Test that delete_task prints confirmation message with task details"""
    # Arrange: Create a task
    task = add_task("Task to confirm", "Confirmation test")
    task_id = task['id']

    # Act: Delete the task
    delete_task(task_id)

    # Assert: Confirmation message printed
    captured = capsys.readouterr()
    assert f"✓ Task #{task_id} deleted: Task to confirm" in captured.out
```

**Run test (should PASS with current implementation)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_prints_confirmation_message -v
```

### Phase 3: Error Handling (User Story 2 - Priority P2)

**Goal**: Handle invalid task IDs gracefully

#### Step 3.1: RED - Test Non-Existent Task ID Raises ValueError

```python
def test_delete_task_raises_error_for_nonexistent_id():
    """Test that delete_task raises ValueError when task ID doesn't exist"""
    # Arrange: Create some tasks (but not ID 999)
    add_task("Task 1", "First")
    add_task("Task 2", "Second")

    # Act & Assert: Deleting non-existent ID raises ValueError
    with pytest.raises(ValueError) as exc_info:
        delete_task(999)

    assert "Task #999 not found" in str(exc_info.value)
```

**Run test (should PASS with current implementation)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_raises_error_for_nonexistent_id -v
```

#### Step 3.2: RED - Test Error Message Printed for Non-Existent ID

```python
def test_delete_task_prints_error_for_nonexistent_id(capsys):
    """Test that delete_task prints error message when task not found"""
    # Arrange: Create a task (ID will be 1)
    add_task("Task 1", "First")

    # Act: Try to delete non-existent task
    with pytest.raises(ValueError):
        delete_task(999)

    # Assert: Error message printed
    captured = capsys.readouterr()
    assert "✗ Error: Task #999 not found" in captured.out
```

**Run test (should PASS with current implementation)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_prints_error_for_nonexistent_id -v
```

#### Step 3.3: RED - Test Storage Unchanged After Error

```python
def test_delete_task_leaves_storage_unchanged_on_error():
    """Test that delete_task doesn't modify storage when task not found"""
    # Arrange: Create tasks
    task1 = add_task("Task 1", "First")
    task2 = add_task("Task 2", "Second")

    from src.storage import _tasks
    initial_count = len(_tasks)

    # Act: Try to delete non-existent task
    with pytest.raises(ValueError):
        delete_task(999)

    # Assert: Storage unchanged
    assert len(_tasks) == initial_count
    assert any(t.id == task1['id'] for t in _tasks)
    assert any(t.id == task2['id'] for t in _tasks)
```

**Run test (should PASS with current implementation)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_leaves_storage_unchanged_on_error -v
```

#### Step 3.4: RED - Test Double Deletion (Delete Already Deleted Task)

```python
def test_delete_task_fails_on_double_deletion():
    """Test that deleting the same task twice raises error on second attempt"""
    # Arrange: Create and delete a task
    task = add_task("Task to delete twice", "Double deletion test")
    task_id = task['id']
    delete_task(task_id)

    # Act & Assert: Second deletion raises ValueError
    with pytest.raises(ValueError) as exc_info:
        delete_task(task_id)

    assert f"Task #{task_id} not found" in str(exc_info.value)
```

**Run test (should PASS with current implementation)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_fails_on_double_deletion -v
```

### Phase 4: Edge Cases

**Goal**: Verify behavior in edge scenarios

#### Step 4.1: RED - Test Delete Only Task (Empty Storage After)

```python
def test_delete_task_works_with_single_task():
    """Test that deleting the only task leaves storage empty"""
    # Arrange: Create one task
    task = add_task("Only task", "Single task")
    task_id = task['id']

    # Act: Delete the only task
    deleted = delete_task(task_id)

    # Assert: Storage is empty
    from src.storage import _tasks
    assert len(_tasks) == 0
    assert deleted['title'] == "Only task"
```

**Run test (should PASS)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_works_with_single_task -v
```

#### Step 4.2: RED - Test Delete First Task (Index 0)

```python
def test_delete_task_handles_first_task():
    """Test that deleting the first task works correctly"""
    # Arrange: Create multiple tasks
    task1 = add_task("First", "Index 0")
    task2 = add_task("Second", "Index 1")
    task3 = add_task("Third", "Index 2")

    # Act: Delete first task
    delete_task(task1['id'])

    # Assert: Other tasks remain
    from src.storage import _tasks
    assert len(_tasks) == 2
    assert _tasks[0].id == task2['id']
    assert _tasks[1].id == task3['id']
```

**Run test (should PASS)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_handles_first_task -v
```

#### Step 4.3: RED - Test Delete Last Task

```python
def test_delete_task_handles_last_task():
    """Test that deleting the last task works correctly"""
    # Arrange: Create multiple tasks
    task1 = add_task("First", "Index 0")
    task2 = add_task("Second", "Index 1")
    task3 = add_task("Third", "Index 2")

    # Act: Delete last task
    delete_task(task3['id'])

    # Assert: Other tasks remain
    from src.storage import _tasks
    assert len(_tasks) == 2
    assert _tasks[0].id == task1['id']
    assert _tasks[1].id == task2['id']
```

**Run test (should PASS)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_handles_last_task -v
```

#### Step 4.4: RED - Test Empty Storage Delete Attempt

```python
def test_delete_task_fails_on_empty_storage():
    """Test that delete_task raises error when storage is empty"""
    # Arrange: Ensure storage is empty (autouse fixture does this)
    from src.storage import _tasks
    assert len(_tasks) == 0

    # Act & Assert: Deleting from empty storage raises ValueError
    with pytest.raises(ValueError) as exc_info:
        delete_task(1)

    assert "Task #1 not found" in str(exc_info.value)
```

**Run test (should PASS)**:
```bash
pytest tests/unit/test_task_manager.py::test_delete_task_fails_on_empty_storage -v
```

### Phase 5: Integration Tests

**Goal**: Verify delete_task integrates with other features

#### Step 5.1: RED - Test Delete Task Created by add_task

```python
# tests/integration/test_delete_task_flow.py

import pytest
from src.task_manager import add_task, delete_task
from src.storage import reset_storage

@pytest.fixture(autouse=True)
def reset_test_storage():
    """Reset storage before each test"""
    reset_storage()
    yield
    reset_storage()

def test_delete_task_works_with_add_task():
    """Integration: delete_task removes tasks created by add_task"""
    # Arrange: Use add_task to create tasks
    task1 = add_task("Task from add_task", "Integration test")
    task2 = add_task("Another task", "Second task")

    # Act: Delete first task
    deleted = delete_task(task1['id'])

    # Assert: Task deleted successfully
    assert deleted['id'] == task1['id']
    assert deleted['title'] == "Task from add_task"

    # Verify second task unaffected
    from src.storage import _tasks
    assert len(_tasks) == 1
    assert _tasks[0].id == task2['id']
```

**Run test**:
```bash
pytest tests/integration/test_delete_task_flow.py::test_delete_task_works_with_add_task -v
```

#### Step 5.2: RED - Test Delete Task Modified by toggle_task_completion

```python
def test_delete_task_works_with_toggled_task():
    """Integration: delete_task can delete tasks modified by toggle_task_completion"""
    # Arrange: Create and toggle a task
    task = add_task("Task to toggle and delete", "Integration")
    task_id = task['id']

    # Toggle completion
    from src.task_manager import toggle_task_completion
    toggle_task_completion(task_id)

    # Act: Delete the toggled task
    deleted = delete_task(task_id)

    # Assert: Deletion successful, captured completed=True state
    assert deleted['id'] == task_id
    assert deleted['completed'] is True  # Captured after toggle

    # Verify storage empty
    from src.storage import _tasks
    assert len(_tasks) == 0
```

**Run test**:
```bash
pytest tests/integration/test_delete_task_flow.py::test_delete_task_works_with_toggled_task -v
```

#### Step 5.3: RED - Test ID Reuse Prevention After Deletion

```python
def test_deleted_ids_are_not_reused():
    """Integration: Verify deleted task IDs are never reused by add_task"""
    # Arrange: Create tasks with IDs 1, 2, 3
    task1 = add_task("Task 1", "First")
    task2 = add_task("Task 2", "Second")
    task3 = add_task("Task 3", "Third")

    # Act: Delete task #2
    delete_task(task2['id'])

    # Create new task (should get ID 4, not reuse ID 2)
    task4 = add_task("Task 4", "Fourth")

    # Assert: New task has ID 4, not 2
    assert task4['id'] == 4
    assert task4['id'] != task2['id']

    # Verify storage has tasks 1, 3, 4 (not 2)
    from src.storage import _tasks
    task_ids = [t.id for t in _tasks]
    assert task_ids == [1, 3, 4]
```

**Run test (should PASS if add_task counter logic is correct)**:
```bash
pytest tests/integration/test_delete_task_flow.py::test_deleted_ids_are_not_reused -v
```

### Phase 6: Performance Validation

**Goal**: Verify deletion completes within 10ms (SC-006)

#### Step 6.1: Performance Test

```python
# tests/integration/test_delete_task_flow.py

import time

def test_delete_task_performance():
    """Performance: Verify delete completes in <10ms for 100 tasks"""
    # Arrange: Create 100 tasks
    task_ids = []
    for i in range(100):
        task = add_task(f"Task {i}", f"Description {i}")
        task_ids.append(task['id'])

    # Act: Time deletion of middle task
    target_id = task_ids[50]
    start_time = time.perf_counter()
    delete_task(target_id)
    end_time = time.perf_counter()

    # Assert: Deletion took less than 10ms
    elapsed_ms = (end_time - start_time) * 1000
    assert elapsed_ms < 10, f"Deletion took {elapsed_ms:.2f}ms, expected <10ms"
```

**Run test**:
```bash
pytest tests/integration/test_delete_task_flow.py::test_delete_task_performance -v
```

### Phase 7: Final Verification

**Goal**: Run all tests and verify feature is complete

#### Step 7.1: Run All Tests

```bash
# Run all tests for this feature
pytest tests/unit/test_task_manager.py -v -k delete

# Run all integration tests
pytest tests/integration/test_delete_task_flow.py -v

# Run entire test suite (including previous features)
pytest tests/ -v
```

#### Step 7.2: Verify Test Coverage

```bash
# Generate coverage report
pytest tests/ --cov=src --cov-report=term-missing

# Verify delete_task function has 100% coverage
# Lines in src/task_manager.py::delete_task should all be covered
```

## Refactoring Opportunities

After all tests pass, consider these refactoring opportunities:

### 1. Extract Task Lookup Helper (DRY Principle)

If you notice task lookup code duplicated across add_task, toggle_task_completion, and delete_task:

```python
# src/task_manager.py

def _find_task_by_id(task_id: int) -> Task | None:
    """Find a task by its ID in storage.

    Args:
        task_id: The ID to search for

    Returns:
        Task object if found, None otherwise
    """
    for task in _tasks:
        if task.id == task_id:
            return task
    return None

# Then update delete_task to use helper:
def delete_task(task_id: int) -> dict[str, Any]:
    task = _find_task_by_id(task_id)

    if task is None:
        print(f"✗ Error: Task #{task_id} not found")
        raise ValueError(f"Task #{task_id} not found")

    # ... rest of implementation
```

**IMPORTANT**: Only refactor if tests still pass after changes.

### 2. Extract Error Handling Pattern (DRY Principle)

If error handling is duplicated across functions:

```python
def _raise_task_not_found(task_id: int) -> None:
    """Raise ValueError for non-existent task ID with console output."""
    print(f"✗ Error: Task #{task_id} not found")
    raise ValueError(f"Task #{task_id} not found")
```

**IMPORTANT**: Only refactor if it improves readability without adding complexity.

## Troubleshooting

### Common Issues

#### Issue: Import Error for delete_task

**Symptom**: `ImportError: cannot import name 'delete_task'`

**Solution**: Ensure delete_task is defined in `src/task_manager.py` and has proper imports

#### Issue: Test Fails with "Task not found" but task exists

**Symptom**: Test creates task but delete_task can't find it

**Solution**: Verify storage is properly reset between tests using `@pytest.fixture(autouse=True)`

#### Issue: Return dictionary missing fields

**Symptom**: KeyError when accessing fields in returned dictionary

**Solution**: Verify all 5 fields are captured: id, title, description, completed, created_at

#### Issue: Other tasks affected by deletion

**Symptom**: Tests show tasks other than target are modified or removed

**Solution**: Use `_tasks.remove(task)` not `del _tasks[index]` without proper tracking

## Success Criteria Checklist

After implementation, verify all success criteria from spec.md:

- [ ] **SC-001**: Users can delete any existing task by ID in a single function call
- [ ] **SC-002**: Deleted tasks are permanently removed from storage and cannot be retrieved
- [ ] **SC-003**: System returns complete task information before deletion for audit purposes
- [ ] **SC-004**: Deletion of one task does not affect other tasks in storage
- [ ] **SC-005**: System handles non-existent task IDs gracefully with clear error messages
- [ ] **SC-006**: Delete operation completes in under 10ms for typical use cases

## Next Steps

After completing implementation and all tests pass:

1. **Create commit**: Use git commit with descriptive message and Co-Authored-By line
2. **Integration testing**: Test with real workflows (add → toggle → delete sequences)
3. **Documentation**: Update any user-facing documentation if needed
4. **Code review**: Review implementation against spec requirements
5. **Prepare PR**: Create pull request following project guidelines

## References

- **Spec**: [spec.md](./spec.md) - Feature requirements and acceptance criteria
- **Plan**: [plan.md](./plan.md) - Implementation approach and architecture
- **Research**: [research.md](./research.md) - Technical decisions and rationale
- **Data Model**: [data-model.md](./data-model.md) - Entity definitions and contracts
- **Constitution**: `.specify/memory/constitution.md` - Project principles and standards
- **001-add-task**: Previous feature implementation for reference
- **002-mark-complete**: Previous feature for task lookup patterns
