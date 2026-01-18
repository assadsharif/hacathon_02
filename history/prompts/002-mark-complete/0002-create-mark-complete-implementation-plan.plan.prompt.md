---
id: 0002
title: create-mark-complete-implementation-plan
stage: plan
date: 2026-01-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-mark-complete
branch: 002-mark-complete
user: asad
command: /sp.plan
labels: ["planning", "architecture", "mark-complete", "toggle-completion", "design"]
links:
  spec: specs/002-mark-complete/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-mark-complete/plan.md
 - specs/002-mark-complete/research.md
 - specs/002-mark-complete/data-model.md
 - specs/002-mark-complete/quickstart.md
 - CLAUDE.md
tests:
 - No tests yet (planning phase)
---

## Prompt

yes, proceed with planning

## Response snapshot

Successfully created comprehensive implementation plan for 002-mark-complete feature following Spec-Driven Development (SDD) methodology with complete Phase 0 (Research) and Phase 1 (Design) documentation.

### Plan Structure

**Main Plan Document** (plan.md):
- **Summary**: Task completion toggle feature building on 001-add-task infrastructure
- **Technical Context**: Python 3.13+, stdlib only, in-memory storage (reuses 001-add-task)
- **Constitution Check**: All 6 checks PASS (specification-first, in-memory only, quality standards, no external deps, SDD workflow, test-first)
- **Project Structure**: Single project, extends src/task_manager.py, no changes to models.py or storage.py
- **Complexity Tracking**: No violations - all constitution principles satisfied

**Phase 0: Research** (research.md):
- **5 Research Questions Answered**:
  1. Data Model: Reuse Task as-is (completed field already exists)
  2. Task Lookup: Linear search O(n) sufficient at scale (<1000 tasks)
  3. Toggle Implementation: Direct boolean negation (`task.completed = not task.completed`)
  4. Error Handling: ValueError with descriptive message (consistent with add_task)
  5. Output Pattern: Dual output (print message + return dictionary)
- **No New ADRs Required**: Reuses ADR-0001, ADR-0002, ADR-0003 from 001-add-task
- **Performance Analysis**: <10ms target with 10x safety margin at expected scale

**Phase 1: Design** (data-model.md):
- **Data Model**: Task entity unchanged, only `completed` field modified by toggle
- **Field Preservation**: Explicit guarantees that id, title, description, created_at remain unchanged
- **Function Contract**: Detailed preconditions, postconditions, side effects, exceptions
- **Validation**: Input (task_id), Output (dictionary format), Invariant checks
- **Performance**: O(n) search + O(1) toggle = O(n) total (~1-2ms for 500 tasks)
- **Integration**: Perfect compatibility with 001-add-task infrastructure

**Phase 1: Quickstart** (quickstart.md):
- **TDD Workflow**: Complete RED-GREEN-REFACTOR guide with 8 phases
- **Step-by-step Implementation**: From function stub to full implementation
- **Test Examples**: 16+ tests covering happy path, bidirectional toggle, field preservation, error handling, messages, integration, edge cases
- **Verification Checklist**: Code quality, functionality, testing, documentation
- **Success Criteria Validation**: All 6 SC mapped to specific tests

### Key Design Decisions

1. **Infrastructure Reuse**: No changes to Task dataclass or storage - completed field already exists
2. **Linear Search**: Simple O(n) lookup sufficient for scale; avoids over-engineering
3. **Direct Negation**: `task.completed = not task.completed` - clear, atomic, idiomatic Python
4. **Consistent Error Handling**: ValueError pattern from add_task maintained
5. **Dual Output Pattern**: Print confirmation + return dictionary (matches add_task)
6. **Status-Based Messages**: Different confirmation for complete vs incomplete state
7. **Field Immutability**: Only completed changes; all other fields explicitly preserved

### Implementation Strategy

**Estimated Complexity**: ~25-32 tasks (40% fewer than 001-add-task due to infrastructure reuse)

**Phase Breakdown**:
- Phase 1: Setup (~2 tasks) - Test infrastructure verification
- Phase 2: Foundation (~1 task) - Import existing infrastructure
- Phase 3: Core Toggle (~12-15 tasks) - US1 (P1) bidirectional toggle
- Phase 4: Error Handling (~5-7 tasks) - US2 (P2) invalid ID handling
- Phase 5: Polish (~5-7 tasks) - Edge cases, performance, validation

**TDD Approach**:
- RED: Write failing tests first
- GREEN: Minimal implementation to pass
- REFACTOR: Clean up while tests pass
- Integration: Tests demonstrate add_task + toggle_task_completion work together

### Risk Assessment

**Low-Risk Decisions**:
- Reuse existing dataclass (no schema changes)
- Linear search (simple, deterministic, testable)
- Boolean negation (atomic, no race conditions)

**Mitigated Risks**:
- Task not found: Clear error handling with ValueError
- Performance: O(n) acceptable at scale (<1000 tasks)
- Field preservation: Explicit testing ensures only completed changes

**Integration Risks**:
- Dependency on 001-add-task: Integration tests validate both features work together
- Storage consistency: Reusing _tasks list ensures no state divergence
- Type compatibility: Using existing Task ensures perfect compatibility

### Constitution Compliance

**All Gates Pass**:
- ✅ Specification-First: Complete spec.md with 2 user stories, 10 FRs, 6 SCs
- ✅ In-Memory Only: Reuses existing storage, no persistence
- ✅ Quality Standards: PEP 8, type hints, docstrings enforced
- ✅ No External Dependencies: Python stdlib only
- ✅ SDD Workflow: Spec → Plan → Tasks → Implementation
- ✅ Test-First: RED-GREEN-REFACTOR TDD cycle

**No Complexity Violations**: Feature minimizes complexity by reusing all infrastructure from 001-add-task

### Dependencies

**Required (from 001-add-task)**:
- src/models.py - Task dataclass with completed field
- src/storage.py - _tasks list for task storage
- tests/conftest.py - pytest fixtures
- test infrastructure - pytest configuration

**Verification Steps**:
1. Ensure 001-add-task tests pass before starting
2. Run 001-add-task tests to verify foundation stable
3. Create integration tests using both features

## Outcome

- ✅ Impact: Complete implementation plan created with Phase 0 (research.md with 5 technical decisions), Phase 1 (data-model.md with contracts and quickstart.md with TDD guide), Phase 2 (task estimation ~25-32 tasks); planning enables tasks generation and implementation
- 🧪 Tests: No tests yet (planning phase); test strategy documented in quickstart.md with 16+ test examples covering all scenarios
- 📁 Files: 4 files created (plan.md, research.md, data-model.md, quickstart.md); CLAUDE.md updated with active technologies
- 🔁 Next prompts: Ready for /sp.tasks to generate detailed task breakdown; then /sp.implement to begin TDD workflow; no clarifications needed
- 🧠 Reflection: Plan significantly simpler than 001-add-task due to infrastructure reuse; all architectural decisions from 001-add-task apply (no new ADRs); linear search acceptable at scale; field preservation critical for correctness (FR-007); integration testing essential to validate both features work together; TDD guide provides complete implementation path with test examples; constitution compliance 100%; estimated 40% fewer tasks than 001-add-task; ready for task generation

## Evaluation notes (flywheel)

- Failure modes observed: None - planning complete on first pass; all research questions answered; all design decisions documented; no architectural ambiguities; constitution checks all pass
- Graders run and results (PASS/FAIL): PASS - All constitution gates passed; technical context complete; research comprehensive (5 questions with alternatives); data model documented with contracts; quickstart provides complete TDD guide; performance analyzed (<10ms target met); integration strategy defined; no complexity violations
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
