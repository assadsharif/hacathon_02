# ADR-0001: Python Union Type Syntax for Optional Values

> **Scope**: This ADR documents the decision to use Python 3.13+ union type syntax (`str | None`) for optional type hints throughout the codebase.

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 001-add-task
- **Context:** The Task dataclass requires type hints for optional fields (e.g., `description` can be a string or None). Python offers multiple syntaxes for expressing optional types, and we needed to choose one consistent approach for the entire codebase.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - affects all future type hints
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - Union, Optional, no hints
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - applies to all typed code
-->

## Decision

**Use Python 3.13+ union type syntax (`str | None`) for all optional type hints.**

This means:
- Optional string: `str | None` (not `Optional[str]`)
- Optional integer: `int | None` (not `Optional[int]`)
- Multiple unions: `str | int | None` (not `Union[str, int, None]`)

**Applies to:**
- All dataclass field annotations
- All function parameter annotations
- All function return type annotations
- All variable type hints

**Example implementation:**
```python
@dataclass
class Task:
    id: int
    title: str
    description: str | None  # ✓ Use this
    # description: Optional[str]  # ✗ Not this
    completed: bool
    created_at: datetime
```

## Consequences

### Positive

- **Modern and Pythonic:** Follows PEP 604 (introduced in Python 3.10, standard in 3.13+)
- **Concise and readable:** `str | None` is more intuitive than `Optional[str]`
- **Symmetric syntax:** Matches set union operator semantics (`|`)
- **No import required:** Built-in syntax, no need to import from `typing`
- **IDE support:** Full support in modern IDEs (PyCharm, VS Code with Pylance)
- **Type checker compatibility:** Works with mypy, pyright, and other type checkers
- **Future-proof:** Recommended syntax in Python 3.10+ documentation
- **Consistency:** Single syntax for all union types (not mixing Optional and Union)

### Negative

- **Python version constraint:** Requires Python 3.10+ (our project uses 3.13+, so acceptable)
- **Not backward compatible:** Code won't run on Python 3.9 or earlier
- **Team familiarity:** Developers used to older syntax may need brief adjustment period
- **Legacy code migration:** Existing codebases using `Optional` would need updating
- **Documentation gap:** Some older tutorials/examples still use `Optional[T]` syntax

**Mitigation:**
- Constitution already mandates Python 3.13+, so version constraint is acceptable
- Team documentation and code reviews will reinforce consistent usage
- Linter/formatter configuration can enforce this style

## Alternatives Considered

### Alternative 1: `Optional[str]` from typing module

**Syntax:**
```python
from typing import Optional

description: Optional[str]
```

**Pros:**
- Traditional Python typing approach (Python 3.5+)
- More explicit about "optional" semantics
- Familiar to developers from older codebases
- Backward compatible with Python 3.5-3.9

**Cons:**
- Requires import from `typing` module
- More verbose than union syntax
- `Optional[T]` is actually `Union[T, None]` under the hood (less honest syntax)
- Not the recommended approach in modern Python

**Why rejected:** Less concise and requires unnecessary imports. Python 3.10+ recommends union syntax.

### Alternative 2: `Union[str, None]` from typing module

**Syntax:**
```python
from typing import Union

description: Union[str, None]
```

**Pros:**
- Explicit union semantics
- Works for complex unions (3+ types)
- Backward compatible

**Cons:**
- Most verbose option
- Requires import
- Redundant when `str | None` syntax exists
- Less readable

**Why rejected:** Most verbose option with no benefits over union syntax in Python 3.10+.

### Alternative 3: No type hints

**Syntax:**
```python
def add_task(title, description=None):
    ...
```

**Pros:**
- No syntax to learn
- Maximum compatibility
- Faster to write

**Cons:**
- No static type checking
- Poor IDE autocompletion
- Violates constitution quality standards (requires type hints)
- Harder to catch bugs before runtime
- Poor documentation for API consumers

**Why rejected:** Constitution mandates type hints for all functions. Type safety is a project requirement.

## References

- Feature Spec: [specs/001-add-task/spec.md](../../specs/001-add-task/spec.md)
- Implementation Plan: [specs/001-add-task/plan.md](../../specs/001-add-task/plan.md)
- Research Document: [specs/001-add-task/research.md](../../specs/001-add-task/research.md#1-data-model-python-dataclass)
- Data Model: [specs/001-add-task/data-model.md](../../specs/001-add-task/data-model.md)
- PEP 604: https://peps.python.org/pep-0604/
- Python 3.10+ Type Hints: https://docs.python.org/3/library/stdtypes.html#types-union
- Related ADRs: ADR-0002 (uses this syntax in storage module), ADR-0003 (uses this syntax in ID generation)
