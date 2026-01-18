"""Integration tests for update_task() flow (001-update-task feature).

This module tests update_task() integration with existing features:
- add_task() → update_task() workflow
- Multiple tasks updated independently
- update_task() + toggle_task_completion() interaction

Test Organization:
- TestUpdateTaskFlow: Integration tests for US1

References:
- Spec: specs/001-update-task/spec.md
- Plan: specs/001-update-task/plan.md
- Tasks: specs/001-update-task/tasks.md (T023-T025)
"""
import pytest
from src.task_manager import add_task, update_task, toggle_task_completion
from src.storage import _tasks


class TestUpdateTaskFlow:
    """Test User Story 1 integration with existing features."""

    def test_add_task_to_update_task_flow(self, capsys):
        """T023 [P] [US1]: Test add_task → update_task workflow.

        Integration test verifying update_task works seamlessly with add_task.

        Spec: Integration requirement (tasks.md T023)
        Given: User creates task with add_task
        When: User updates task with update_task
        Then: Task is updated successfully with correct field preservation
        """
        # ARRANGE: Create task with add_task
        task = add_task("Initial Title", "Initial Description")
        task_id = task['id']
        original_id = task['id']
        original_completed = task['completed']
        original_created_at = task['created_at']
        capsys.readouterr()  # Clear add_task output

        # ACT: Update task title
        result = update_task(task_id, title="Updated Title")
        captured = capsys.readouterr()

        # ASSERT: Title updated, description preserved
        assert result['title'] == "Updated Title", "Title should be updated"
        assert result['description'] == "Initial Description", "Description should be preserved"

        # ASSERT: Immutable fields preserved
        assert result['id'] == original_id, "ID should be preserved"
        assert result['completed'] == original_completed, "Completed should be preserved"
        assert result['created_at'] == original_created_at, "created_at should be preserved"

        # ASSERT: Confirmation message displayed
        assert f"✓ Task #{task_id} updated successfully" in captured.out

        # ACT: Update description
        result2 = update_task(task_id, description="Updated Description")
        captured2 = capsys.readouterr()

        # ASSERT: Description updated, title preserved from previous update
        assert result2['title'] == "Updated Title", "Title should be preserved from previous update"
        assert result2['description'] == "Updated Description", "Description should be updated"

        # ASSERT: Immutable fields still preserved
        assert result2['id'] == original_id, "ID should still be preserved"
        assert result2['completed'] == original_completed, "Completed should still be preserved"
        assert result2['created_at'] == original_created_at, "created_at should still be preserved"

        # ASSERT: Confirmation message displayed
        assert f"✓ Task #{task_id} updated successfully" in captured2.out

        # ACT: Update both fields
        result3 = update_task(task_id, title="Final Title", description="Final Description")

        # ASSERT: Both fields updated
        assert result3['title'] == "Final Title"
        assert result3['description'] == "Final Description"

        # ASSERT: Task in storage matches final state
        stored_task = _tasks[0]
        assert stored_task.id == task_id
        assert stored_task.title == "Final Title"
        assert stored_task.description == "Final Description"
        assert stored_task.completed == original_completed
        assert stored_task.created_at == original_created_at

    def test_multiple_tasks_updated_independently(self, capsys):
        """T024 [P] [US1]: Test multiple tasks updated independently.

        Integration test verifying update_task doesn't affect other tasks.

        Spec: Integration requirement (tasks.md T024)
        Given: Multiple tasks exist
        When: Update one task
        Then: Only that task is updated, others remain unchanged
        """
        # ARRANGE: Create three tasks
        task1 = add_task("Task 1", "Description 1")
        task2 = add_task("Task 2", "Description 2")
        task3 = add_task("Task 3", "Description 3")

        task1_id = task1['id']
        task2_id = task2['id']
        task3_id = task3['id']

        # Store original values
        task1_original_title = task1['title']
        task1_original_description = task1['description']
        task2_original_title = task2['title']
        task2_original_description = task2['description']
        task3_original_title = task3['title']
        task3_original_description = task3['description']

        capsys.readouterr()  # Clear add_task outputs

        # ACT: Update task2 only
        result = update_task(task2_id, title="Updated Task 2")

        # ASSERT: Task 2 updated
        assert result['title'] == "Updated Task 2"
        assert result['description'] == task2_original_description

        # ASSERT: Task 1 unchanged
        assert _tasks[0].id == task1_id
        assert _tasks[0].title == task1_original_title
        assert _tasks[0].description == task1_original_description

        # ASSERT: Task 3 unchanged
        assert _tasks[2].id == task3_id
        assert _tasks[2].title == task3_original_title
        assert _tasks[2].description == task3_original_description

        # ACT: Update task1 and task3
        result1 = update_task(task1_id, description="New Description 1")
        result3 = update_task(task3_id, title="Updated Task 3", description="New Description 3")

        # ASSERT: All tasks have correct values
        assert _tasks[0].title == task1_original_title  # Unchanged
        assert _tasks[0].description == "New Description 1"  # Updated

        assert _tasks[1].title == "Updated Task 2"  # From previous update
        assert _tasks[1].description == task2_original_description  # Unchanged

        assert _tasks[2].title == "Updated Task 3"  # Updated
        assert _tasks[2].description == "New Description 3"  # Updated

        # ASSERT: All tasks have correct IDs
        assert _tasks[0].id == task1_id
        assert _tasks[1].id == task2_id
        assert _tasks[2].id == task3_id

    def test_update_task_with_toggle_completion(self, capsys):
        """T025 [US1]: Test update_task + toggle_task_completion interaction.

        Integration test verifying update_task and toggle_task_completion work together.

        Spec: Integration requirement (implicit in tasks.md T025)
        Given: Task exists
        When: Update task, toggle completion, update again
        Then: All operations succeed, completed field preserved during update
        """
        # ARRANGE: Create task
        task = add_task("Task to Update and Complete", "Description")
        task_id = task['id']
        original_created_at = task['created_at']
        capsys.readouterr()  # Clear add_task output

        # ACT: Update task (while incomplete)
        result1 = update_task(task_id, title="Updated Title")

        # ASSERT: Task updated, still incomplete
        assert result1['title'] == "Updated Title"
        assert result1['completed'] is False

        # ACT: Toggle completion to True
        result2 = toggle_task_completion(task_id)
        capsys.readouterr()  # Clear toggle output

        # ASSERT: Task marked complete
        assert result2['completed'] is True
        assert result2['title'] == "Updated Title"  # Title preserved

        # ACT: Update task again (while completed)
        result3 = update_task(task_id, description="New Description")

        # ASSERT: Description updated, completed status PRESERVED (not changed by update_task)
        assert result3['description'] == "New Description"
        assert result3['title'] == "Updated Title"
        assert result3['completed'] is True, "Completed status should be preserved during update"

        # ACT: Toggle completion back to False
        result4 = toggle_task_completion(task_id)

        # ASSERT: Task marked incomplete
        assert result4['completed'] is False
        assert result4['title'] == "Updated Title"
        assert result4['description'] == "New Description"

        # ASSERT: Immutable fields never changed
        assert result1['id'] == task_id
        assert result2['id'] == task_id
        assert result3['id'] == task_id
        assert result4['id'] == task_id

        assert result1['created_at'] == original_created_at
        assert result2['created_at'] == original_created_at
        assert result3['created_at'] == original_created_at
        assert result4['created_at'] == original_created_at
