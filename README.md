# Todo Application - Menu-Driven Interface

A fully-featured, in-memory todo application with 7 core features and an intuitive numbered menu interface.

## Features

```
==================================================
TODO APPLICATION
==================================================
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Search / Filter Tasks
7. Sort Tasks
8. Exit
==================================================
```

## Quick Start

```bash
# Run the application
python3 main.py

# Or with uv
uv run python main.py
```

## All 7 Features

### 1. ✅ Add Task
Create new todo items with title and optional description.

### 2. 📋 View All Tasks
Display all tasks with full details.

### 3. ✏️ Update Task
Modify existing task title or description.

### 4. ❌ Delete Task
Remove tasks with confirmation.

### 5. ✓ Toggle Task Completion
Switch tasks between complete/incomplete.

### 6. 🔍 Search / Filter Tasks
Search by keyword and filter by status (all/completed/incomplete).

### 7. 📊 Sort Tasks
Sort by ID, title, created date, or status.

## Testing

```bash
# Test all features
python3 test_all_features.py      # Features 1-5 (24 tests)
python3 test_search_sort.py        # Features 6-7 (13 tests)
```

**Result**: ✅ ALL 37 TESTS PASSED!

## Technology Stack

- **Language**: Python 3.13+
- **Package Manager**: UV
- **Dependencies**: Zero (Python stdlib only)
- **Storage**: In-memory

## Important Notes

⚠️ **In-Memory Only**: All data lost on exit (by design).

✅ **All Features**: 7 complete features
✅ **37 Tests**: All passing
✅ **Spec-Driven**: 6 feature specifications
✅ **Clean Code**: PEP 8, type hints, comprehensive tests
