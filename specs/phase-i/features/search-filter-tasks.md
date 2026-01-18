# Feature Specification: Search / Filter Tasks

## Feature Name
**Search / Filter Tasks**

## User Story
As a user, I want to search and filter my tasks so I can quickly find specific tasks based on keywords or completion status.

## Acceptance Criteria

### AC1: Search by Keyword
- User can search tasks by keyword in title or description
- Search is case-insensitive
- Returns all tasks that contain the keyword

### AC2: Filter by Completion Status
- User can filter tasks by completion status
- Options: All, Completed, Incomplete
- Returns only tasks matching the selected status

### AC3: Combined Search and Filter
- User can combine keyword search with status filter
- Both criteria must be satisfied

### AC4: Display Results
- Display matching tasks with same format as View All Tasks
- Show count of matching tasks
- If no matches, display appropriate message

## Technical Specification

### Function Signature
```python
def search_tasks(
    keyword: str | None = None,
    status_filter: str = "all"
) -> list[Task]:
    """
    Search and filter tasks.

    Args:
        keyword: Search keyword (searches in title and description)
        status_filter: Filter by status ("all", "completed", "incomplete")

    Returns:
        List of Task objects matching the criteria
    """
    pass
```

## Testing Scenarios

### Test Case 1: Search by Keyword
```python
# Setup
add_task("Buy groceries")
add_task("Call dentist")
add_task("Buy flowers")

# Input
keyword = "buy"

# Expected
Returns 2 tasks: "Buy groceries" and "Buy flowers"
```

### Test Case 2: Filter by Completed
```python
# Setup
add_task("Buy groceries")
add_task("Call dentist")
toggle_task_completion(1)

# Input
status_filter = "completed"

# Expected
Returns 1 task: "Buy groceries" (completed)
```

### Test Case 3: Combined Search and Filter
```python
# Input
keyword = "buy"
status_filter = "incomplete"

# Expected
Returns only incomplete tasks containing "buy"
```

## Success Criteria
- ✅ Search is case-insensitive
- ✅ Searches both title and description
- ✅ Filter by status works correctly
- ✅ Combined search and filter works
- ✅ Returns empty list when no matches
