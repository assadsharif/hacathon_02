# ADR-0003: Sequential Counter-Based ID Generation

> **Scope**: This ADR documents the decision to use a module-level counter with increment-before-assign pattern for generating unique task IDs.

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 001-add-task
- **Context:** FR-004 requires each task to have a unique sequential integer ID starting from 1. We needed to choose an ID generation strategy that guarantees uniqueness, maintains sequential order, and integrates simply with in-memory storage.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - affects ID collision strategy
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - counter vs UUID vs timestamp
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - all entities will need IDs
-->

## Decision

**Use a module-level counter (`_task_id_counter: int = 0`) with increment-before-assign pattern for ID generation.**

**Implementation components:**
- **Counter variable:** `_task_id_counter: int = 0` (module-level in `src/storage.py`)
- **Generation function:** `_generate_task_id() -> int` (increments counter, returns new value)
- **Pattern:** Increment BEFORE assignment (counter starts at 0, first ID is 1)
- **Scope:** Private module function (prefixed with `_`)

**Example implementation:**
```python
# src/storage.py
_task_id_counter: int = 0

def _generate_task_id() -> int:
    """Generate next sequential task ID.

    Returns:
        Next unique task ID (starting from 1)
    """
    global _task_id_counter
    _task_id_counter += 1
    return _task_id_counter
```

**Usage pattern:**
```python
# src/task_manager.py
def add_task(title: str, description: str | None = None) -> dict:
    task_id = _generate_task_id()  # Gets 1, then 2, then 3, etc.
    task = Task(
        id=task_id,
        title=title,
        description=description,
        completed=False,
        created_at=datetime.now()
    )
    _tasks.append(task)
    return task
```

## Consequences

### Positive

- **Simplicity:** Single integer counter, minimal code
- **Sequential:** IDs are 1, 2, 3, ... (user-friendly and predictable)
- **User-friendly:** Small integers are easy to reference ("Task #5")
- **Performance:** O(1) ID generation (just increment)
- **Guaranteed uniqueness:** Counter never decrements or repeats
- **Meets FR-004:** Satisfies "unique sequential integer ID starting from 1"
- **No dependencies:** Pure Python, no external packages
- **Deterministic:** Same sequence every run (helpful for testing)
- **Debuggable:** Easy to reason about ID assignment order

### Negative

- **Not distributed-safe:** Multiple processes would have ID collisions
- **Not thread-safe:** Concurrent access needs locking (acceptable per A3: single-threaded)
- **Resets on restart:** IDs start from 1 again when app restarts (acceptable: no persistence)
- **No collision detection:** Assumes single-threaded, single-process (per constitution)
- **Not cryptographically secure:** IDs are predictable (not a concern: single-user console app)
- **Future migration:** Moving to distributed system or database would require new strategy

**Mitigation:**
- Constitution assumption A3 states single-threaded operation
- In-memory storage means restart resets all data anyway (IDs resetting is consistent)
- If Phase II adds persistence, ID generation will be revisited in new ADR

## Alternatives Considered

### Alternative 1: UUID (Universally Unique Identifier)

**Syntax:**
```python
import uuid
task_id = str(uuid.uuid4())  # e.g., "550e8400-e29b-41d4-a716-446655440000"
```

**Pros:**
- Globally unique (no collisions even across processes/machines)
- Distributed-system safe
- Cryptographically secure (UUID4)
- No coordination needed between processes

**Cons:**
- Not sequential (random order)
- Not user-friendly (long strings, hard to reference: "Task #550e8400...")
- Violates FR-004 requirement: "sequential integer ID"
- String type instead of integer
- Overkill for single-user console app

**Why rejected:** Doesn't meet FR-004 requirement for sequential integer IDs. UUIDs are optimized for distributed systems, but we have a single-threaded, single-process console app. The long string format is not user-friendly for console display.

### Alternative 2: Timestamp-based IDs

**Syntax:**
```python
from datetime import datetime
task_id = int(datetime.now().timestamp() * 1000000)  # Microsecond precision
```

**Pros:**
- Roughly chronological
- Sortable by creation time
- No global counter needed

**Cons:**
- Not truly sequential (gaps between values)
- Risk of collisions if tasks created in same microsecond
- Not starting from 1 (violates FR-004)
- Harder to read (e.g., ID = 1736780400000000)
- Clock changes cause issues (DST, NTP sync)

**Why rejected:** Doesn't guarantee uniqueness (collision risk) and doesn't meet FR-004 requirement for sequential IDs starting from 1. Timestamp IDs are not user-friendly for console display.

### Alternative 3: `len(tasks) + 1`

**Syntax:**
```python
task_id = len(_tasks) + 1
```

**Pros:**
- No separate counter needed
- Simple one-liner
- Sequential and user-friendly

**Cons:**
- Breaks if tasks are deleted (out of scope but future consideration)
- Can result in ID reuse (e.g., delete task 5, next task also gets ID 5)
- Couples ID generation to list length (bad separation of concerns)
- Not robust for future extensibility

**Why rejected:** Although simple, this approach is fragile for future features. If future phases add task deletion, IDs would be reused, breaking uniqueness. Separate counter is more robust and follows single-responsibility principle (ID generation is independent of storage).

### Alternative 4: Database auto-increment

**Syntax:**
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
);
```

**Pros:**
- Standard pattern in SQL databases
- Thread-safe and transaction-safe
- Built-in to most databases

**Cons:**
- Requires database (violates FR-006: in-memory only)
- External dependency (violates constitution)
- Massive overkill for in-memory console app
- Constitution explicitly prohibits database operations

**Why rejected:** Constitution requires in-memory-only storage with no database. If Phase II adds persistence, database auto-increment will be considered in that ADR, but it's not appropriate for Phase I.

## References

- Feature Spec: [specs/001-add-task/spec.md](../../specs/001-add-task/spec.md) (FR-004: sequential ID requirement)
- Implementation Plan: [specs/001-add-task/plan.md](../../specs/001-add-task/plan.md)
- Research Document: [specs/001-add-task/research.md](../../specs/001-add-task/research.md#2-id-generation-strategy)
- Data Model: [specs/001-add-task/data-model.md](../../specs/001-add-task/data-model.md#id-counter)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (assumption A3: single-threaded)
- Related ADRs: ADR-0001 (type hints for counter), ADR-0002 (storage integration)
