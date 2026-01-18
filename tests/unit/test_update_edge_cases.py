"""Edge case and performance tests for update_task() (001-update-task feature).

This module tests edge cases and performance requirements:
- Long titles (1000+ characters)
- Special characters (emojis, unicode)
- Rapid successive updates
- Invalid combinations (both fields provided but title invalid)
- Performance (< 10ms execution per SC-006)

Test Organization:
- TestUpdateTaskEdgeCases: Boundary conditions
- TestUpdateTaskPerformance: Performance validation

References:
- Spec: specs/001-update-task/spec.md (SC-006: Performance)
- Tasks: specs/001-update-task/tasks.md (T043-T049)
"""
import pytest
import time
from src.task_manager import add_task, update_task
from src.storage import _tasks


class TestUpdateTaskEdgeCases:
    """Test edge cases and boundary conditions for update_task."""

    def test_long_title_1000_plus_characters(self):
        """T043 [P]: Long title (1000+ characters) handled correctly.

        Edge Case: System should handle very long titles
        Given: Task exists
        When: update_task() with 1000+ character title
        Then: Title updated successfully, no truncation or errors
        """
        # ARRANGE: Create task
        task = add_task("Original Title", "Description")
        task_id = task['id']

        # Create 1000+ character title
        long_title = "A" * 1500

        # ACT: Update with long title
        result = update_task(task_id, title=long_title)

        # ASSERT: Long title stored correctly
        assert result['title'] == long_title, "Long title should be stored without truncation"
        assert len(result['title']) == 1500, "Title length should be 1500"
        assert _tasks[0].title == long_title, "Storage should contain full long title"

    def test_special_characters_emojis_unicode(self):
        """T044 [P]: Special characters (emojis, unicode) handled correctly.

        Edge Case: System should handle unicode, emojis, special characters
        Given: Task exists
        When: update_task() with emojis and unicode
        Then: Title and description updated with special characters preserved
        """
        # ARRANGE: Create task
        task = add_task("Original", "Description")
        task_id = task['id']

        # Special character test cases
        emoji_title = "🚀 Task with emojis 🎉 完成"
        unicode_description = "Ñoño: 日本語 Русский العربية 中文 한국어"

        # ACT: Update with emojis and unicode
        result = update_task(task_id, title=emoji_title, description=unicode_description)

        # ASSERT: Special characters preserved
        assert result['title'] == emoji_title, "Emoji and unicode title should be preserved"
        assert result['description'] == unicode_description, "Unicode description should be preserved"
        assert _tasks[0].title == emoji_title, "Storage should preserve emojis"
        assert _tasks[0].description == unicode_description, "Storage should preserve unicode"

    def test_rapid_successive_updates(self):
        """T045 [P]: Rapid successive updates work correctly.

        Edge Case: Multiple rapid updates should all succeed
        Given: Task exists
        When: Multiple update_task() calls in quick succession
        Then: All updates succeed, final state reflects last update
        """
        # ARRANGE: Create task
        task = add_task("Initial", "Initial")
        task_id = task['id']

        # ACT: Perform 10 rapid successive updates
        for i in range(10):
            result = update_task(task_id, title=f"Title {i}", description=f"Description {i}")

        # ASSERT: Final state is the last update (i=9)
        assert result['title'] == "Title 9", "Final title should be from last update"
        assert result['description'] == "Description 9", "Final description should be from last update"
        assert _tasks[0].title == "Title 9", "Storage should reflect final update"
        assert _tasks[0].description == "Description 9", "Storage should reflect final update"

        # ACT: Rapid updates alternating fields
        for i in range(5):
            update_task(task_id, title=f"Rapid Title {i}")
            update_task(task_id, description=f"Rapid Desc {i}")

        final = update_task(task_id, title="Final Title", description="Final Desc")

        # ASSERT: Final state correct
        assert final['title'] == "Final Title"
        assert final['description'] == "Final Desc"

    def test_both_fields_provided_but_title_invalid(self, capsys):
        """T046 [P]: Both fields provided but title invalid - proper error handling.

        Edge Case: When both fields provided but title is invalid
        Given: Task exists
        When: update_task(id, title="", description="Valid")
        Then: ValueError raised, neither field updated (atomic validation)
        """
        # ARRANGE: Create task
        task = add_task("Original Title", "Original Description")
        task_id = task['id']
        original_title = task['title']
        original_description = task['description']
        capsys.readouterr()  # Clear add_task output

        # ACT & ASSERT: Empty title with valid description should fail
        with pytest.raises(ValueError, match=r"Task title cannot be empty"):
            update_task(task_id, title="", description="New Description")

        # ASSERT: Neither field updated (atomicity)
        assert _tasks[0].title == original_title, "Title should be unchanged after validation error"
        assert _tasks[0].description == original_description, "Description should not be updated when validation fails"

        # ACT & ASSERT: Whitespace title with valid description should fail
        with pytest.raises(ValueError, match=r"Task title cannot be empty"):
            update_task(task_id, title="   ", description="Another Description")

        # ASSERT: Still unchanged
        assert _tasks[0].title == original_title, "Title should still be unchanged"
        assert _tasks[0].description == original_description, "Description should still be unchanged"

        # ACT: Now update with BOTH fields valid
        result = update_task(task_id, title="New Valid Title", description="New Valid Description")

        # ASSERT: Both updated successfully
        assert result['title'] == "New Valid Title"
        assert result['description'] == "New Valid Description"


class TestUpdateTaskPerformance:
    """Test performance requirements for update_task."""

    def test_update_task_performance_under_10ms(self):
        """T048 [P]: update_task() completes in < 10ms (SC-006).

        Performance Requirement: SC-006 from spec.md
        Given: Task exists
        When: update_task() is called
        Then: Execution completes in < 10ms (10000 microseconds)
        """
        # ARRANGE: Create task
        task = add_task("Task for Performance Test", "Description")
        task_id = task['id']

        # Warm-up call (exclude first call from measurement due to potential caching effects)
        update_task(task_id, title="Warmup")

        # ACT: Measure execution time for title update
        start_time = time.perf_counter()
        update_task(task_id, title="Performance Test Title")
        end_time = time.perf_counter()
        title_update_time_ms = (end_time - start_time) * 1000

        # ACT: Measure execution time for description update
        start_time = time.perf_counter()
        update_task(task_id, description="Performance Test Description")
        end_time = time.perf_counter()
        description_update_time_ms = (end_time - start_time) * 1000

        # ACT: Measure execution time for both fields update
        start_time = time.perf_counter()
        update_task(task_id, title="Both Fields", description="Both Updated")
        end_time = time.perf_counter()
        both_fields_time_ms = (end_time - start_time) * 1000

        # ASSERT: All operations complete in < 10ms (SC-006)
        assert title_update_time_ms < 10.0, \
            f"Title update took {title_update_time_ms:.3f}ms, should be < 10ms (SC-006)"
        assert description_update_time_ms < 10.0, \
            f"Description update took {description_update_time_ms:.3f}ms, should be < 10ms (SC-006)"
        assert both_fields_time_ms < 10.0, \
            f"Both fields update took {both_fields_time_ms:.3f}ms, should be < 10ms (SC-006)"

        # Print timing info for visibility (not part of assertion)
        print(f"\nPerformance Results (SC-006 requires < 10ms):")
        print(f"  Title update: {title_update_time_ms:.3f}ms")
        print(f"  Description update: {description_update_time_ms:.3f}ms")
        print(f"  Both fields update: {both_fields_time_ms:.3f}ms")

    def test_performance_with_large_task_list(self):
        """T049: Performance with larger task list (100 tasks).

        Performance scalability check
        Given: 100 tasks exist
        When: update_task() on last task
        Then: Still completes in < 10ms (linear search through 100 items)
        """
        # ARRANGE: Create 100 tasks
        task_ids = []
        for i in range(100):
            task = add_task(f"Task {i}", f"Description {i}")
            task_ids.append(task['id'])

        # Target last task (worst case for linear search)
        last_task_id = task_ids[-1]

        # Warm-up
        update_task(last_task_id, title="Warmup")

        # ACT: Measure update on last task (worst case)
        start_time = time.perf_counter()
        update_task(last_task_id, title="Updated Last Task")
        end_time = time.perf_counter()
        update_time_ms = (end_time - start_time) * 1000

        # ASSERT: Still under 10ms even with 100 tasks
        assert update_time_ms < 10.0, \
            f"Update with 100 tasks took {update_time_ms:.3f}ms, should be < 10ms (SC-006)"

        print(f"\nPerformance with 100 tasks: {update_time_ms:.3f}ms")
