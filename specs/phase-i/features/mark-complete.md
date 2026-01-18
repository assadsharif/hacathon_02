# Feature Specification: Mark as Complete

## Feature Name
**Mark as Complete**

## User Story
As a user, I want to mark a task as complete or incomplete so I can track my progress.

## Acceptance Criteria

### AC1: Task ID Required
- User must provide a task ID
- ID must be an integer
- Task with the specified ID must exist

### AC2: Toggle Completion Status
- If task is incomplete (completed=False), mark as complete (completed=True)
- If task is complete (completed=True), mark as incomplete (completed=False)
- Toggle behavior allows marking and unmarking

### AC3: Task Updated in Storage
- The task's completed field is updated in memory
- All other fields remain unchanged (id, title, description, created_at)

### AC4: Confirmation Message
- Upon successful toggle, display confirmation message
- Message should indicate new status
- Format when marking complete: `"✓ Task #{id} marked as complete"`
- Format when marking incomplete: `"✓ Task #{id} marked as incomplete"`

### AC5: Error Handling
- If task ID does not exist, display error: `"✗ Error: Task #{id} not found"`
- If ID is invalid (not a number), display error: `"✗ Error: Invalid task ID"`

## Technical Specification

### Function Signature
```python
def toggle_task_completion(task_id: int) -> dict[str, Any]:
    """
    Toggle the completion status of a task.

    Args:
        task_id: The unique task identifier

    Returns:
        Dictionary containing updated task details:
        {
            'id': int,
            'title': str,
            'description': str | None,
            'completed': bool,  # Toggled value
            'created_at': datetime
        }

    Raises:
        ValueError: If task with specified ID does not exist
    """
    pass
```

## Testing Scenarios

### Test Case 1: Mark Incomplete Task as Complete
```python
# Setup
add_task("Buy groceries")  # ID: 1, completed=False

# Input
toggle_task_completion(task_id=1)

# Expected Output
{
    'id': 1,
    'title': "Buy groceries",
    'description': None,
    'completed': True,  # Changed from False to True
    'created_at': <original_datetime>
}

# Expected Console Output
"✓ Task #1 marked as complete"
```

### Test Case 2: Mark Complete Task as Incomplete
```python
# Setup
task = add_task("Buy groceries")  # ID: 1
toggle_task_completion(1)  # Now completed=True

# Input
toggle_task_completion(task_id=1)

# Expected Output
{
    'id': 1,
    'title': "Buy groceries",
    'description': None,
    'completed': False,  # Changed from True to False
    'created_at': <original_datetime>
}

# Expected Console Output
"✓ Task #1 marked as incomplete"
```

### Test Case 3: Toggle Non-Existent Task
```python
# Input
toggle_task_completion(task_id=999)

# Expected Behavior
- Raise ValueError
- Console Output: "✗ Error: Task #999 not found"
```

### Test Case 4: Multiple Toggles
```python
# Setup
add_task("Buy groceries")  # ID: 1, completed=False

# Toggle 1
toggle_task_completion(1)  # completed=True

# Toggle 2
toggle_task_completion(1)  # completed=False

# Toggle 3
toggle_task_completion(1)  # completed=True

# Expected
Task should be completed=True after 3 toggles
```

## Display Enhancement

When displaying tasks in the list, use visual indicators:
- Incomplete tasks: `○` (empty circle)
- Complete tasks: `✓` (checkmark)

Example:
```
--- All Tasks (2) ---

✓ Task #1: Buy groceries
  Created: 2026-01-04 21:00:00

○ Task #2: Call dentist
  Created: 2026-01-04 21:05:00
```

## Success Criteria
- ✅ Function signature matches specification
- ✅ All acceptance criteria met
- ✅ All test cases pass
- ✅ Toggle behavior works correctly
- ✅ Visual indicators in task list
- ✅ Error handling works correctly
