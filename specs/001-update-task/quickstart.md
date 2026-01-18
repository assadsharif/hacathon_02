# Quickstart Guide: Update Task

**Feature**: 001-update-task
**Date**: 2026-01-14
**Purpose**: Fast-start guide for using and testing the update_task feature

---

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Common Patterns](#common-patterns)
3. [Error Handling](#error-handling)
4. [Integration Examples](#integration-examples)
5. [Running Tests](#running-tests)

---

## Basic Usage

### Update Title Only

```python
from src.task_manager import add_task, update_task

# Create a task
task = add_task("Original Title", "Original Description")
# ✓ Task #1 added: Original Title

# Update only the title
updated = update_task(1, title="New Title")
# ✓ Task #1 updated successfully

print(updated['title'])        # "New Title"
print(updated['description'])  # "Original Description" (unchanged)
print(updated['id'])           # 1 (unchanged)
print(updated['created_at'])   # Original timestamp (unchanged)
```

### Update Description Only

```python
# Update only the description
updated = update_task(1, description="New Description")
# ✓ Task #1 updated successfully

print(updated['title'])        # "New Title" (unchanged)
print(updated['description'])  # "New Description"
```

### Update Both Fields

```python
# Update both title and description
updated = update_task(1, title="Final Title", description="Final Description")
# ✓ Task #1 updated successfully

print(updated['title'])        # "Final Title"
print(updated['description'])  # "Final Description"
```

### Clear Description

```python
# Clear the description (set to None)
updated = update_task(1, description=None)
# ✓ Task #1 updated successfully

print(updated['description'])  # None
```

---

## Common Patterns

### Pattern 1: Iterative Refinement

```python
# Create initial task
task = add_task("Draft report")
# ✓ Task #1 added: Draft report

# Add description later
update_task(1, description="Q4 financial report")
# ✓ Task #1 updated successfully

# Refine title based on feedback
update_task(1, title="Draft Q4 Financial Report")
# ✓ Task #1 updated successfully

# Add more details to description
update_task(1, description="Q4 financial report - due Friday")
# ✓ Task #1 updated successfully
```

### Pattern 2: Whitespace Normalization

```python
# Title with leading/trailing whitespace is automatically cleaned
task = add_task("   Messy Title   ")
# ✓ Task #1 added: Messy Title
# (whitespace stripped automatically)

# Same normalization happens on update
update_task(1, title="  Cleaned Title  ")
# ✓ Task #1 updated successfully

print(task['title'])  # "Cleaned Title" (no extra spaces)
```

### Pattern 3: Preserving Completion Status

```python
from src.task_manager import toggle_task_completion

# Create and complete a task
task = add_task("Completed Task", "Done")
toggle_task_completion(1)
# ✓ Task #1 marked as complete

# Update the task - completion status is preserved
update_task(1, title="Updated Completed Task")
# ✓ Task #1 updated successfully

print(task['completed'])  # True (still completed)
```

### Pattern 4: Multiple Tasks

```python
# Create multiple tasks
task1 = add_task("Task 1", "First task")
task2 = add_task("Task 2", "Second task")
task3 = add_task("Task 3", "Third task")

# Update them independently
update_task(1, title="Updated Task 1")
# ✓ Task #1 updated successfully

update_task(3, description="Updated third task")
# ✓ Task #3 updated successfully

# Task 2 remains unchanged
```

---

## Error Handling

### Error 1: No Fields Provided

```python
try:
    update_task(1)  # Neither title nor description provided
except ValueError as e:
    print(f"Error: {e}")

# Console output:
# ✗ Error: No fields to update
# Error: No fields to update
```

**Solution**: Provide at least one field to update:
```python
update_task(1, title="New Title")  # ✅ Correct
```

### Error 2: Task Not Found

```python
try:
    update_task(999, title="New Title")  # Task 999 doesn't exist
except ValueError as e:
    print(f"Error: {e}")

# Console output:
# ✗ Error: Task #999 not found
# Error: Task #999 not found
```

**Solution**: Use a valid task ID:
```python
# Check existing tasks first
task = add_task("Valid Task")
update_task(task['id'], title="Updated")  # ✅ Correct
```

### Error 3: Empty Title

```python
try:
    update_task(1, title="")  # Empty title
except ValueError as e:
    print(f"Error: {e}")

# Console output:
# ✗ Error: Task title cannot be empty
# Error: Task title cannot be empty

try:
    update_task(1, title="   ")  # Whitespace-only title
except ValueError as e:
    print(f"Error: {e}")

# Console output:
# ✗ Error: Task title cannot be empty
# Error: Task title cannot be empty
```

**Solution**: Provide a non-empty title:
```python
update_task(1, title="Valid Title")  # ✅ Correct
```

### Error Handling Best Practice

```python
def safe_update_task(task_id, title=None, description=None):
    """Wrapper with error handling."""
    try:
        result = update_task(task_id, title=title, description=description)
        print(f"✅ Successfully updated task {task_id}")
        return result
    except ValueError as e:
        print(f"❌ Update failed: {e}")
        return None

# Usage
result = safe_update_task(1, title="New Title")
if result:
    print(f"Updated task: {result['title']}")
else:
    print("Update failed, check error message above")
```

---

## Integration Examples

### Example 1: Create → Update → Complete Workflow

```python
from src.task_manager import add_task, update_task, toggle_task_completion

# Step 1: Create task
task = add_task("Draft proposal")
# ✓ Task #1 added: Draft proposal

# Step 2: Add details
update_task(1, description="Client proposal for Project X")
# ✓ Task #1 updated successfully

# Step 3: Refine title
update_task(1, title="Draft Client Proposal - Project X")
# ✓ Task #1 updated successfully

# Step 4: Mark complete when done
toggle_task_completion(1)
# ✓ Task #1 marked as complete

# Final state: Completed task with refined details
print(f"Task: {task['title']}")
print(f"Description: {task['description']}")
print(f"Completed: {task['completed']}")
```

### Example 2: Batch Updates

```python
# Create multiple tasks
tasks = [
    add_task("Task 1", "Description 1"),
    add_task("Task 2", "Description 2"),
    add_task("Task 3", "Description 3"),
]

# Update all titles with a prefix
for i, task in enumerate(tasks, 1):
    update_task(task['id'], title=f"[URGENT] Task {i}")
    # ✓ Task #1 updated successfully
    # ✓ Task #2 updated successfully
    # ✓ Task #3 updated successfully
```

### Example 3: Conditional Updates

```python
from src.task_manager import add_task, update_task

# Create task
task = add_task("Research topic", None)  # No description initially

# Later: Add description if we have details
details = input("Enter task details (or press Enter to skip): ")
if details:
    update_task(task['id'], description=details)
    print("Description added!")
else:
    print("No description added.")
```

---

## Running Tests

### Prerequisites

```bash
# Ensure you have pytest installed
pip install pytest pytest-cov
```

### Run All Tests

```bash
# Run all update_task tests
pytest tests/unit/test_update_task.py -v
pytest tests/unit/test_update_edge_cases.py -v
pytest tests/integration/test_update_task_flow.py -v
```

### Run Specific Test Categories

```bash
# Unit tests only (core functionality)
pytest tests/unit/test_update_task.py -v

# Edge cases only
pytest tests/unit/test_update_edge_cases.py -v

# Integration tests only
pytest tests/integration/test_update_task_flow.py -v
```

### Run Tests with Coverage

```bash
# Generate coverage report
pytest tests/ -v --cov=src.task_manager --cov-report=term-missing

# Expected output:
# src/task_manager.py    100%
```

### Run Specific Test

```bash
# Run a single test by name
pytest tests/unit/test_update_task.py::TestUpdateTaskUS1::test_update_title_only -v

# Run all tests in a class
pytest tests/unit/test_update_task.py::TestUpdateTaskUS1 -v
```

### Performance Testing

```bash
# Run performance tests
pytest tests/unit/test_update_edge_cases.py::TestUpdatePerformance -v

# Expected: All updates complete in < 10ms
```

---

## Troubleshooting

### Issue: "AttributeError: 'NoneType' object has no attribute 'title'"

**Cause**: Trying to access task fields when task doesn't exist

**Solution**:
```python
# Bad
task = update_task(999, title="New")  # Raises ValueError
print(task['title'])  # Never reached

# Good
try:
    task = update_task(1, title="New")
    print(task['title'])
except ValueError as e:
    print(f"Task not found: {e}")
```

### Issue: "ValueError: No fields to update"

**Cause**: Calling update_task without providing title or description

**Solution**:
```python
# Bad
update_task(1)  # Error: no fields

# Good
update_task(1, title="New")  # ✅ Updates title
update_task(1, description="New")  # ✅ Updates description
update_task(1, title="T", description="D")  # ✅ Updates both
```

### Issue: Title gets stripped unexpectedly

**Cause**: Leading/trailing whitespace is automatically removed (by design)

**Explanation**: This is intentional behavior to ensure data quality
```python
update_task(1, title="  Spaced  ")
# Result: title = "Spaced" (whitespace removed)
```

### Issue: Can't update completion status

**Cause**: update_task only modifies title and description

**Solution**: Use toggle_task_completion for completion status
```python
# Bad
# update_task(1, completed=True)  # Not supported

# Good
toggle_task_completion(1)  # ✅ Correct way to change completion
```

---

## Quick Reference

### Function Signature

```python
update_task(task_id: int, *, title: str | None = None, description: str | None = None) -> dict[str, Any]
```

### Valid Calls

```python
update_task(1, title="New Title")
update_task(1, description="New Description")
update_task(1, title="T", description="D")
update_task(1, description=None)  # Clear description
```

### Invalid Calls

```python
update_task(1)  # ❌ No fields
update_task(1, "Title")  # ❌ Must use keyword argument
update_task(1, title="")  # ❌ Empty title
update_task(999, title="T")  # ❌ Task doesn't exist
```

### Return Value Structure

```python
{
    'id': int,               # Task ID
    'title': str,            # Current title
    'description': str | None,  # Current description (can be None)
    'completed': bool,       # Completion status
    'created_at': datetime   # Creation timestamp
}
```

### Error Messages

- `"✗ Error: No fields to update"` → Provide title and/or description
- `"✗ Error: Task #X not found"` → Use valid task ID
- `"✗ Error: Task title cannot be empty"` → Provide non-empty title

---

## Next Steps

1. ✅ Read the [specification](./spec.md) for complete requirements
2. ✅ Review [API contract](./contracts/update_task.md) for detailed behavior
3. ✅ Check [data model](./data-model.md) for field semantics
4. ⏳ Run tests to validate implementation
5. ⏳ Implement your own update workflows

**Happy coding!** 🚀
