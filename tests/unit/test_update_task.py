"""Unit tests for update_task() function (001-update-task feature).

This module tests the update_task() functionality following TDD (RED-GREEN-REFACTOR).
Tests are written FIRST and must FAIL before implementation.

Test Organization:
- TestUpdateTaskUS1: Core update functionality (P1)
- TestUpdateTaskUS2: Error handling (P2) - in separate phase
- TestUpdateTaskOutput: Output validation

References:
- Spec: specs/001-update-task/spec.md
- Plan: specs/001-update-task/plan.md
- Contracts: specs/001-update-task/contracts/update_task.md
"""
import pytest
from src.task_manager import add_task, update_task
from src.storage import _tasks


class TestUpdateTaskUS1:
    """Test User Story 1: Update Task Fields (Priority: P1).

    Core functionality - update title and/or description while preserving
    immutable fields (id, completed, created_at).
    """

    def test_update_title_only(self, capsys):
        """T006 [P] [US1]: Update title only, description preserved.

        Spec: FR-001, FR-002, FR-006, FR-009, FR-010
        Given: Task exists with title "Old Title" and description "Old Description"
        When: update_task(task_id, title="New Title")
        Then: Title updated, description unchanged, confirmation message displayed
        """
        # ARRANGE: Create initial task
        task = add_task("Old Title", "Old Description")
        task_id = task['id']
        original_description = task['description']
        original_completed = task['completed']
        original_created_at = task['created_at']
        capsys.readouterr()  # Clear add_task output

        # ACT: Update title only
        result = update_task(task_id, title="New Title")
        captured = capsys.readouterr()

        # ASSERT: Title updated
        assert result['title'] == "New Title", "Title should be updated"

        # ASSERT: Description preserved
        assert result['description'] == original_description, "Description should be unchanged"

        # ASSERT: Immutable fields preserved
        assert result['id'] == task_id, "ID should be unchanged"
        assert result['completed'] == original_completed, "Completed should be unchanged"
        assert result['created_at'] == original_created_at, "created_at should be unchanged"

        # ASSERT: Confirmation message displayed
        assert f"✓ Task #{task_id} updated successfully" in captured.out, \
            "Should display success message"

    def test_update_description_only(self, capsys):
        """T007 [P] [US1]: Update description only, title preserved.

        Spec: FR-001, FR-002, FR-006, FR-009, FR-010
        Given: Task exists with title "Task Title" and description "Original"
        When: update_task(task_id, description="Updated Description")
        Then: Description updated, title unchanged, confirmation message displayed
        """
        # ARRANGE: Create initial task
        task = add_task("Task Title", "Original")
        task_id = task['id']
        original_title = task['title']
        original_completed = task['completed']
        original_created_at = task['created_at']
        capsys.readouterr()  # Clear add_task output

        # ACT: Update description only
        result = update_task(task_id, description="Updated Description")
        captured = capsys.readouterr()

        # ASSERT: Description updated
        assert result['description'] == "Updated Description", "Description should be updated"

        # ASSERT: Title preserved
        assert result['title'] == original_title, "Title should be unchanged"

        # ASSERT: Immutable fields preserved
        assert result['id'] == task_id, "ID should be unchanged"
        assert result['completed'] == original_completed, "Completed should be unchanged"
        assert result['created_at'] == original_created_at, "created_at should be unchanged"

        # ASSERT: Confirmation message displayed
        assert f"✓ Task #{task_id} updated successfully" in captured.out, \
            "Should display success message"

    def test_update_both_fields(self, capsys):
        """T008 [P] [US1]: Update both title and description.

        Spec: FR-001, FR-002, FR-006, FR-009, FR-010
        Given: Task exists with title "Old" and description "Old"
        When: update_task(task_id, title="New", description="New")
        Then: Both fields updated, confirmation message displayed
        """
        # ARRANGE: Create initial task
        task = add_task("Old", "Old")
        task_id = task['id']
        original_completed = task['completed']
        original_created_at = task['created_at']
        capsys.readouterr()  # Clear add_task output

        # ACT: Update both fields
        result = update_task(task_id, title="New", description="New")
        captured = capsys.readouterr()

        # ASSERT: Both fields updated
        assert result['title'] == "New", "Title should be updated"
        assert result['description'] == "New", "Description should be updated"

        # ASSERT: Immutable fields preserved
        assert result['id'] == task_id, "ID should be unchanged"
        assert result['completed'] == original_completed, "Completed should be unchanged"
        assert result['created_at'] == original_created_at, "created_at should be unchanged"

        # ASSERT: Confirmation message displayed
        assert f"✓ Task #{task_id} updated successfully" in captured.out, \
            "Should display success message"

    def test_immutable_fields_preserved(self):
        """T009 [P] [US1]: Immutable fields (id, completed, created_at) preserved.

        Spec: FR-007
        Given: Task exists
        When: update_task() is called
        Then: id, completed, created_at remain unchanged
        """
        # ARRANGE: Create initial task
        task1 = add_task("Task 1", "Description 1")
        task2 = add_task("Task 2", "Description 2")

        # Store original immutable values
        original_id = task1['id']
        original_completed = task1['completed']
        original_created_at = task1['created_at']

        # ACT: Update task
        result = update_task(task1['id'], title="Updated", description="Updated")

        # ASSERT: Immutable fields unchanged
        assert result['id'] == original_id, "ID must never change"
        assert result['completed'] == original_completed, "Completed must not change (use toggle_task_completion)"
        assert result['created_at'] == original_created_at, "created_at must never change"

        # ASSERT: Task 2 completely unaffected
        assert _tasks[1].id == task2['id'], "Other tasks should be unaffected"
        assert _tasks[1].title == "Task 2", "Other tasks should be unaffected"

    def test_description_cleared_with_none(self):
        """T010 [P] [US1]: Description can be cleared (set to None).

        Spec: FR-008
        Given: Task exists with description "Some description"
        When: update_task(task_id, description=None)
        Then: Description is None, other fields unchanged
        """
        # ARRANGE: Create task with description
        task = add_task("Task", "Some description")
        task_id = task['id']
        original_title = task['title']

        # ACT: Clear description by setting to None
        result = update_task(task_id, description=None)

        # ASSERT: Description is None
        assert result['description'] is None, "Description should be cleared to None"

        # ASSERT: Title unchanged
        assert result['title'] == original_title, "Title should be unchanged"

    def test_whitespace_stripped_from_title(self):
        """T011 [P] [US1]: Whitespace stripped from title.

        Spec: FR-015
        Given: Task exists
        When: update_task(task_id, title="  Spaced Title  ")
        Then: Title stored as "Spaced Title" (whitespace removed)
        """
        # ARRANGE: Create initial task
        task = add_task("Original", None)
        task_id = task['id']

        # ACT: Update with title containing leading/trailing whitespace
        result = update_task(task_id, title="  Spaced Title  ")

        # ASSERT: Whitespace stripped
        assert result['title'] == "Spaced Title", "Leading/trailing whitespace should be stripped"
        assert result['title'] != "  Spaced Title  ", "Should not contain whitespace"

    def test_confirmation_message_displayed(self, capsys):
        """T012 [P] [US1]: Confirmation message displayed on success.

        Spec: FR-009
        Given: Task exists
        When: update_task() succeeds
        Then: Print "✓ Task #{id} updated successfully"
        """
        # ARRANGE: Create task
        task = add_task("Task", None)
        task_id = task['id']
        capsys.readouterr()  # Clear add_task output

        # ACT: Update task
        update_task(task_id, title="Updated")
        captured = capsys.readouterr()

        # ASSERT: Confirmation message
        assert "✓" in captured.out, "Should display success checkmark"
        assert f"Task #{task_id}" in captured.out, "Should include task ID"
        assert "updated successfully" in captured.out, "Should indicate update success"
        assert captured.out.strip() == f"✓ Task #{task_id} updated successfully", \
            "Should match exact message format"

    def test_return_value_structure(self):
        """T013 [P] [US1]: Return dictionary with all task fields.

        Spec: FR-010
        Given: Task exists
        When: update_task() is called
        Then: Return dict with id, title, description, completed, created_at
        """
        # ARRANGE: Create task
        task = add_task("Task", "Description")
        task_id = task['id']

        # ACT: Update task
        result = update_task(task_id, title="Updated")

        # ASSERT: Return value is dict with all fields
        assert isinstance(result, dict), "Should return a dictionary"

        # ASSERT: All required fields present
        required_fields = {'id', 'title', 'description', 'completed', 'created_at'}
        assert set(result.keys()) == required_fields, f"Should have exactly these fields: {required_fields}"

        # ASSERT: Field types
        assert isinstance(result['id'], int), "id should be int"
        assert isinstance(result['title'], str), "title should be str"
        assert result['description'] is None or isinstance(result['description'], str), \
            "description should be str or None"
        assert isinstance(result['completed'], bool), "completed should be bool"
        # Note: created_at type checked in add_task tests


class TestUpdateTaskUS2:
    """Test User Story 2: Handle Invalid Updates (Priority: P2).

    Error handling - validate inputs and provide clear error messages.
    """

    def test_task_not_found_error(self, capsys):
        """T026 [P] [US2]: Task not found error with clear message.

        Spec: FR-003, FR-011, FR-014
        Given: Task with ID 999 does not exist
        When: update_task(999, title="New")
        Then: Display error message and raise ValueError
        """
        # ARRANGE: Ensure task 999 doesn't exist
        # (reset_task_storage fixture ensures empty storage)

        # ACT & ASSERT: Should raise ValueError
        with pytest.raises(ValueError, match=r"Task #999 not found"):
            update_task(999, title="New Title")

        # ASSERT: Error message displayed
        captured = capsys.readouterr()
        assert "✗ Error: Task #999 not found" in captured.out, \
            "Should display error message before raising"

    def test_empty_title_error_empty_string(self, capsys):
        """T027 [P] [US2]: Empty title error (empty string).

        Spec: FR-005, FR-012, FR-014
        Given: Task exists
        When: update_task(task_id, title="")
        Then: Display error message and raise ValueError
        """
        # ARRANGE: Create task
        task = add_task("Original Title", "Description")
        task_id = task['id']
        capsys.readouterr()  # Clear add_task output

        # ACT & ASSERT: Should raise ValueError
        with pytest.raises(ValueError, match=r"Task title cannot be empty"):
            update_task(task_id, title="")

        # ASSERT: Error message displayed
        captured = capsys.readouterr()
        assert "✗ Error: Task title cannot be empty" in captured.out, \
            "Should display error message before raising"

    def test_empty_title_error_whitespace_only(self, capsys):
        """T028 [P] [US2]: Empty title error (whitespace only).

        Spec: FR-005, FR-012, FR-014
        Given: Task exists
        When: update_task(task_id, title="   ")
        Then: Display error message and raise ValueError
        """
        # ARRANGE: Create task
        task = add_task("Original Title", "Description")
        task_id = task['id']
        capsys.readouterr()  # Clear add_task output

        # ACT & ASSERT: Should raise ValueError for whitespace-only title
        with pytest.raises(ValueError, match=r"Task title cannot be empty"):
            update_task(task_id, title="   ")

        # ASSERT: Error message displayed
        captured = capsys.readouterr()
        assert "✗ Error: Task title cannot be empty" in captured.out, \
            "Should display error message before raising"

    def test_no_fields_provided_error(self, capsys):
        """T029 [P] [US2]: No fields provided error.

        Spec: FR-004, FR-013, FR-014
        Given: Task exists
        When: update_task(task_id) with no fields
        Then: Display error message and raise ValueError
        """
        # ARRANGE: Create task
        task = add_task("Title", "Description")
        task_id = task['id']
        capsys.readouterr()  # Clear add_task output

        # ACT & ASSERT: Should raise ValueError
        with pytest.raises(ValueError, match=r"No fields to update"):
            update_task(task_id)

        # ASSERT: Error message displayed
        captured = capsys.readouterr()
        assert "✗ Error: No fields to update" in captured.out, \
            "Should display error message before raising"

    def test_task_unchanged_after_error(self):
        """T030 [P] [US2]: Task unchanged after validation error (atomicity).

        Spec: FR-014 (implicit atomicity requirement)
        Given: Task exists with title "Original"
        When: update_task() raises ValueError (empty title)
        Then: Task remains unchanged in storage
        """
        # ARRANGE: Create task
        task = add_task("Original Title", "Original Description")
        task_id = task['id']
        original_title = task['title']
        original_description = task['description']
        original_completed = task['completed']
        original_created_at = task['created_at']

        # ACT: Try to update with empty title (should fail)
        try:
            update_task(task_id, title="")
        except ValueError:
            pass  # Expected

        # ASSERT: Task unchanged in storage
        assert _tasks[0].id == task_id
        assert _tasks[0].title == original_title, "Title should be unchanged after error"
        assert _tasks[0].description == original_description, "Description should be unchanged after error"
        assert _tasks[0].completed == original_completed, "Completed should be unchanged after error"
        assert _tasks[0].created_at == original_created_at, "created_at should be unchanged after error"

        # ACT: Try to update non-existent task (should fail)
        try:
            update_task(999, title="New Title")
        except ValueError:
            pass  # Expected

        # ASSERT: Existing task still unchanged
        assert _tasks[0].title == original_title, "Task should still be unchanged after second error"

    def test_storage_empty_scenario(self, capsys):
        """T031 [P] [US2]: Storage empty scenario - task not found.

        Spec: FR-003, FR-011
        Given: Storage is empty (no tasks)
        When: update_task(1, title="Title")
        Then: Display error message and raise ValueError
        """
        # ARRANGE: Storage is empty (reset_task_storage fixture ensures this)
        # Verify storage is empty
        assert len(_tasks) == 0, "Storage should be empty"

        # ACT & ASSERT: Should raise ValueError
        with pytest.raises(ValueError, match=r"Task #1 not found"):
            update_task(1, title="New Title")

        # ASSERT: Error message displayed
        captured = capsys.readouterr()
        assert "✗ Error: Task #1 not found" in captured.out, \
            "Should display error message for empty storage"
