# ADR-0002: In-Memory List Storage Architecture

> **Scope**: This ADR documents the decision to use a module-level Python list as the primary storage mechanism for tasks in the Add Task feature.

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 001-add-task
- **Context:** The project constitution mandates in-memory-only storage with no persistence (FR-006). We needed to choose a data structure that balances simplicity, performance, and future extensibility while meeting the "no external dependencies" constraint.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - affects storage layer design
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - list vs dict vs class-based
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - all features interact with storage
-->

## Decision

**Use a module-level Python list (`_tasks: list[Task] = []`) in `src/storage.py` for task storage.**

**Storage components:**
- **Primary storage:** `_tasks: list[Task] = []` (module-level variable)
- **Access pattern:** Direct list operations (append, iterate, index access)
- **Visibility:** Private module variable (prefixed with `_`)
- **Scope:** Module-level (not class-based or function-local)

**Example implementation:**
```python
# src/storage.py
_tasks: list[Task] = []

def get_all_tasks() -> list[Task]:
    return _tasks.copy()

def add_task_to_storage(task: Task) -> None:
    _tasks.append(task)
```

## Consequences

### Positive

- **Simplicity:** Straightforward Python list, no abstraction overhead
- **Constitution compliance:** Satisfies in-memory-only requirement (FR-006)
- **Performance:** O(1) amortized append, sufficient for expected scale (<1000 tasks)
- **Ordered by default:** List maintains insertion order (tasks ordered by creation time)
- **No dependencies:** Pure Python stdlib, no external packages
- **Memory efficient:** List is optimized for sequential access at small-to-medium scale
- **Easy to test:** Simple structure, easy to reset between tests
- **Idiomatic Python:** Uses standard Python data structures

### Negative

- **No persistence:** Data lost on application restart (per design, not a bug)
- **Linear search:** Finding tasks by ID is O(n) (acceptable at expected scale)
- **Memory only:** Entire list must fit in RAM (not a concern for <1000 tasks)
- **Single-threaded:** Not thread-safe (acceptable per assumption A3: single-threaded)
- **No indexing:** No fast lookup by ID without iteration (acceptable tradeoff)
- **Future migration:** If persistence needed later, requires architectural change

**Mitigation:**
- Scale assumptions documented in spec.md (expected <1000 tasks per session)
- Constitution explicitly requires in-memory-only for this phase
- Future features requiring persistence will trigger new ADR and storage refactor

## Alternatives Considered

### Alternative 1: Dictionary (id → Task mapping)

**Syntax:**
```python
_tasks: dict[int, Task] = {}
```

**Pros:**
- O(1) lookup by ID
- Fast existence checks
- Direct access by key

**Cons:**
- Loses insertion order (pre-Python 3.7) or relies on implementation detail
- More complex to iterate in order
- Adds unnecessary complexity for current use case
- No current feature requires ID-based lookup

**Why rejected:** Current feature only appends tasks and doesn't look them up by ID. List iteration is fast enough at expected scale (<1000 items). Dictionary adds complexity without current benefit. If future features require ID lookup, we can add a secondary index without changing primary storage.

### Alternative 2: Class-based singleton storage manager

**Syntax:**
```python
class TaskStorage:
    _instance = None
    _tasks: list[Task] = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
```

**Pros:**
- Encapsulates storage logic
- Could add caching or indexing easily
- More "object-oriented"
- Easier to mock in tests

**Cons:**
- Unnecessary abstraction for simple list management
- More boilerplate code
- Singleton pattern adds complexity
- Violates YAGNI principle (You Aren't Gonna Need It)
- Still module-level state under the hood

**Why rejected:** Adds architectural complexity without solving any current problem. Module-level variables already provide singleton semantics in Python. The class wrapper provides no material benefit for managing a simple list. If we need more sophisticated storage later, we can refactor.

### Alternative 3: Deque (collections.deque)

**Syntax:**
```python
from collections import deque
_tasks: deque[Task] = deque()
```

**Pros:**
- O(1) append and prepend (both ends)
- Thread-safe for append/pop operations
- Optimized for queue operations

**Cons:**
- No random access by index (O(n))
- Optimized for FIFO/LIFO, not our use case
- Less familiar to developers than list
- No current need for queue semantics

**Why rejected:** We don't need queue operations (FIFO/LIFO). Task creation is append-only, and we don't pop from either end. List is simpler and more appropriate for our access pattern.

### Alternative 4: SQLite in-memory database

**Syntax:**
```python
import sqlite3
conn = sqlite3.connect(':memory:')
```

**Pros:**
- SQL query capabilities
- Indexing and relationships
- More scalable
- Familiar to database developers

**Cons:**
- External dependency (violates constitution)
- Massive overkill for simple list
- Requires schema management
- Adds query complexity
- Slower than direct list access
- Constitution explicitly prohibits database

**Why rejected:** Constitution requires no external dependencies beyond stdlib and no database operations. SQLite adds unnecessary complexity for a simple in-memory list. If persistence is needed in Phase II, it will be a new feature with its own ADR.

## References

- Feature Spec: [specs/001-add-task/spec.md](../../specs/001-add-task/spec.md) (FR-006: in-memory requirement)
- Implementation Plan: [specs/001-add-task/plan.md](../../specs/001-add-task/plan.md#technical-context)
- Research Document: [specs/001-add-task/research.md](../../specs/001-add-task/research.md#3-storage-in-memory-list)
- Data Model: [specs/001-add-task/data-model.md](../../specs/001-add-task/data-model.md#storage-schema)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (in-memory requirement)
- Related ADRs: ADR-0001 (type hints), ADR-0003 (ID generation interacts with storage)
