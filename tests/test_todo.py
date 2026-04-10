# =============================================================================
# TESTS/TEST_TODO.PY - Automated Tests for TodoMVC Application
# =============================================================================
# This file contains all automated test cases for the TodoMVC demo.
# Tests cover: adding todos, marking complete, deleting, and filtering.
#
# Each test function follows the Arrange-Act-Assert pattern:
#   - Arrange: Set up the test data and initial state
#   - Act: Perform the action being tested
#   - Assert: Verify the expected outcome
# =============================================================================

# Import the re module for regular expression pattern matching
# Used for flexible text assertions in some tests
import re

# Import pytest for creating fixtures and parametrized tests
import pytest

# Import Playwright's Page class and expect assertion utility
# Page: represents a browser tab
# expect: provides auto-retry assertions for stable tests
from playwright.sync_api import Page, expect

# Import the TodoPage Page Object class
# This provides methods to interact with the TodoMVC UI
from pages.todo_page import TodoPage

# =============================================================================
# TEST FIXTURES
# =============================================================================
# Fixtures provide reusable setup for multiple tests.
# The todo_page fixture creates a TodoPage instance for each test.
# =============================================================================


@pytest.fixture
def todo_page(page: Page) -> TodoPage:
    """
    Fixture that provides a TodoPage instance for tests.

    This fixture creates a new TodoPage object wrapping the Playwright Page.
    The page is already navigated to the base URL by conftest.py.

    Args:
        page: The Playwright Page fixture (injected by pytest-playwright)

    Returns:
        TodoPage: A TodoPage instance ready for interaction
    """
    # Create and return a TodoPage instance with the current page
    return TodoPage(page)


# =============================================================================
# TEST GROUP 1: Adding Todo Items
# =============================================================================
# Tests for requirement: "A new todo item can be added using English text"
# Tests for requirement: "A new todo item can be added using non-English characters"
# Tests for requirement: "A new todo item can be added that includes numbers"
# =============================================================================


def test_add_todo_english(todo_page: TodoPage) -> None:
    """
    Test adding a todo item with English text.

    Requirement: A new todo item can be added using English text.

    This test verifies:
    - A todo with English text can be added
    - The todo appears in the list
    - The todo count updates correctly
    """
    # ARRANGE: Define the todo text to add
    # Using a simple English phrase for this test
    todo_text = "Buy groceries"

    # ACT: Add the todo item using the TodoPage method
    # This types the text and presses Enter
    todo_page.add_todo(todo_text)

    # ASSERT: Verify the todo was added to the list
    # Check that there is exactly 1 todo item visible
    # expect().to_have_count() waits for the condition to be met
    expect(todo_page.todo_items).to_have_count(1)

    # ASSERT: Verify the todo text matches what was entered
    # get_todo_by_index(0) gets the first (and only) todo
    # We check that the label contains the exact text
    first_todo = todo_page.get_todo_by_index(0)
    expect(first_todo.locator("label")).to_have_text(todo_text)

    # ASSERT: Verify the todo count shows 1 item left
    # The count label should display "1 item left"
    expect(todo_page.todo_count_label).to_contain_text("1")


def test_add_todo_non_english(todo_page: TodoPage) -> None:
    """
    Test adding todo items with non-English characters (Unicode support).

    Requirement: A new todo item can be added using non-English characters.

    This test verifies the application handles international characters:
    - Chinese characters (学中文 - learning Chinese)
    - Japanese characters (こんにちは - Hello)
    - Cyrillic characters (Привет - Hello in Russian)
    """
    # ARRANGE: Define todo texts in different languages
    # These represent various Unicode character sets
    chinese_text = "学中文"  # Simplified Chinese characters
    japanese_text = "こんにちは"  # Japanese hiragana
    cyrillic_text = "Привет"  # Russian Cyrillic alphabet

    # ACT: Add all three todos with non-English text
    # Each add_todo call creates a new todo item
    todo_page.add_todo(chinese_text)
    todo_page.add_todo(japanese_text)
    todo_page.add_todo(cyrillic_text)

    # ASSERT: Verify all 3 todos were added
    # The list should contain exactly 3 items
    expect(todo_page.todo_items).to_have_count(3)

    # ASSERT: Verify each todo's text is preserved correctly
    # Check the first todo (Chinese)
    first_todo = todo_page.get_todo_by_index(0)
    expect(first_todo.locator("label")).to_have_text(chinese_text)

    # Check the second todo (Japanese)
    second_todo = todo_page.get_todo_by_index(1)
    expect(second_todo.locator("label")).to_have_text(japanese_text)

    # Check the third todo (Cyrillic)
    third_todo = todo_page.get_todo_by_index(2)
    expect(third_todo.locator("label")).to_have_text(cyrillic_text)

    # ASSERT: Verify the count shows 3 items left
    expect(todo_page.todo_count_label).to_contain_text("3")


def test_add_todo_numbers(todo_page: TodoPage) -> None:
    """
    Test adding a todo item that includes numbers.

    Requirement: A new todo item can be added that includes numbers.

    This test verifies the application correctly handles numeric characters
    mixed with text in todo items.
    """
    # ARRANGE: Define todo text with numbers
    # Using a realistic shopping list with quantities
    todo_text = "Buy 3 apples and 2 bananas"

    # ACT: Add the todo with numbers
    todo_page.add_todo(todo_text)

    # ASSERT: Verify the todo was added
    expect(todo_page.todo_items).to_have_count(1)

    # ASSERT: Verify the text including numbers is preserved correctly
    first_todo = todo_page.get_todo_by_index(0)
    expect(first_todo.locator("label")).to_have_text(todo_text)


# =============================================================================
# TEST GROUP 2: Marking Todos as Complete
# =============================================================================
# Test for requirement: "A todo item can be marked as completed and appears
# correctly in the 'Completed' view"
# =============================================================================


def test_mark_complete_and_view_completed(todo_page: TodoPage) -> None:
    """
    Test marking a todo as complete and viewing it in the Completed filter.

    Requirement: A todo item can be marked as completed and appears correctly
    in the "Completed" view.

    This test verifies:
    - A todo can be marked as complete
    - The completed todo appears in the "Completed" filter view
    - The todo is visually indicated as complete (strikethrough styling)
    - The count of remaining items updates correctly
    """
    # ARRANGE: Add two todos with different texts
    # We'll complete one and leave the other active
    first_todo_text = "Task to complete"
    second_todo_text = "Task to keep active"

    # Add both todos to the list
    todo_page.add_todo(first_todo_text)
    todo_page.add_todo(second_todo_text)

    # Verify both todos exist before proceeding
    expect(todo_page.todo_items).to_have_count(2)

    # ACT: Mark the first todo as complete
    # Index 0 refers to the first todo ("Task to complete")
    todo_page.mark_complete(0)

    # ASSERT: Verify the count shows 1 item left (only the second todo)
    expect(todo_page.todo_count_label).to_contain_text("1")

    # ASSERT: Verify the first todo has the 'completed' class
    # This class controls the visual styling (strikethrough)
    first_todo = todo_page.get_todo_by_index(0)
    expect(first_todo).to_have_class(re.compile("completed"))

    # ACT: Switch to the "Completed" filter view
    # This should show only completed todos
    todo_page.filter_by_completed()

    # ASSERT: Verify only 1 todo is visible (the completed one)
    # The active todo should be hidden in this view
    expect(todo_page.todo_items).to_have_count(1)

    # ASSERT: Verify the visible todo is the completed one
    completed_todo = todo_page.get_todo_by_index(0)
    expect(completed_todo.locator("label")).to_have_text(first_todo_text)

    # ACT: Switch back to "All" view to verify both todos still exist
    todo_page.filter_by_all()

    # ASSERT: Verify both todos are visible in "All" view
    expect(todo_page.todo_items).to_have_count(2)


# =============================================================================
# TEST GROUP 3: Deleting Todo Items
# =============================================================================
# Test for requirement: "A todo item can be deleted and no longer appears
# in any view"
# =============================================================================


def test_delete_todo(todo_page: TodoPage) -> None:
    """
    Test deleting a todo item and verifying it's removed from all views.

    Requirement: A todo item can be deleted and no longer appears in any view.

    This test verifies:
    - A todo can be deleted using the destroy button
    - The deleted todo no longer appears in "All" view
    - The deleted todo no longer appears in "Active" view
    - The deleted todo no longer appears in "Completed" view (if it was complete)
    - The count updates correctly after deletion
    """
    # ARRANGE: Add two todos - one to delete, one to keep
    todo_to_delete = "Todo to delete"
    todo_to_keep = "Todo to keep"

    # Add both todos
    todo_page.add_todo(todo_to_delete)
    todo_page.add_todo(todo_to_keep)

    # Verify both todos exist
    expect(todo_page.todo_items).to_have_count(2)

    # ACT: Delete the first todo (index 0)
    # The delete_todo method handles hovering to reveal the destroy button
    todo_page.delete_todo(0)

    # ASSERT: Verify only 1 todo remains
    expect(todo_page.todo_items).to_have_count(1)

    # ASSERT: Verify the remaining todo is the one we kept
    remaining_todo = todo_page.get_todo_by_index(0)
    expect(remaining_todo.locator("label")).to_have_text(todo_to_keep)

    # ASSERT: Verify the deleted todo no longer exists
    # We use the Page Object method to check by text
    assert not todo_page.todo_exists(todo_to_delete), "Deleted todo should not exist in the list"

    # ASSERT: Verify the count shows 1 item left
    expect(todo_page.todo_count_label).to_contain_text("1")

    # ACT: Switch to "Active" view and verify deleted todo is not there
    todo_page.filter_by_active()

    # ASSERT: In Active view, only the remaining todo should be visible
    expect(todo_page.todo_items).to_have_count(1)
    expect(todo_page.get_todo_by_index(0).locator("label")).to_have_text(todo_to_keep)

    # ACT: Switch to "Completed" view and verify deleted todo is not there
    todo_page.filter_by_completed()

    # ASSERT: In Completed view, no todos should be visible
    # (neither todo was marked as complete before deletion)
    expect(todo_page.todo_items).to_have_count(0)


# =============================================================================
# TEST GROUP 4: Filtering Todos
# =============================================================================
# Test for requirement: "The 'Active' filter correctly shows only items
# that are not completed"
# Test for requirement: "The 'Completed' filter correctly shows only items
# that have been marked as completed"
# =============================================================================


def test_active_filter(todo_page: TodoPage) -> None:
    """
    Test that the "Active" filter shows only incomplete todo items.

    Requirement: The "Active" filter correctly shows only items that are
    not completed.

    This test verifies:
    - Active filter hides completed todos
    - Active filter shows only incomplete todos
    - Switching back to "All" shows all todos again
    """
    # ARRANGE: Create a mix of complete and incomplete todos
    active_todo_1 = "Active task 1"
    active_todo_2 = "Active task 2"
    completed_todo = "Completed task"

    # Add all three todos
    todo_page.add_todo(active_todo_1)
    todo_page.add_todo(completed_todo)
    todo_page.add_todo(active_todo_2)

    # Verify all 3 todos exist
    expect(todo_page.todo_items).to_have_count(3)

    # ACT: Mark the second todo (index 1) as complete
    todo_page.mark_complete(1)

    # ASSERT: Verify count shows 2 items left (2 active, 1 completed)
    expect(todo_page.todo_count_label).to_contain_text("2")

    # ACT: Click the "Active" filter
    todo_page.filter_by_active()

    # ASSERT: Verify only 2 todos are visible (the active ones)
    expect(todo_page.todo_items).to_have_count(2)

    # ASSERT: Verify both visible todos are the active ones
    # We check by text to ensure the correct todos are shown
    first_visible = todo_page.get_todo_by_index(0)
    second_visible = todo_page.get_todo_by_index(1)

    expect(first_visible.locator("label")).to_have_text(active_todo_1)
    expect(second_visible.locator("label")).to_have_text(active_todo_2)

    # ASSERT: Verify the completed todo is NOT visible
    # We check that no todo with the completed text exists
    assert not todo_page.todo_exists(completed_todo), (
        "Completed todo should not appear in Active filter"
    )

    # ACT: Switch back to "All" filter
    todo_page.filter_by_all()

    # ASSERT: Verify all 3 todos are visible again
    expect(todo_page.todo_items).to_have_count(3)


def test_completed_filter(todo_page: TodoPage) -> None:
    """
    Test that the "Completed" filter shows only completed todo items.

    Requirement: The "Completed" filter correctly shows only items that
    have been marked as completed.

    This test verifies:
    - Completed filter shows only completed todos
    - Completed filter hides incomplete (active) todos
    - Switching back to "All" shows all todos again
    """
    # ARRANGE: Create a mix of complete and incomplete todos
    active_todo = "Active task"
    completed_todo_1 = "Completed task 1"
    completed_todo_2 = "Completed task 2"

    # Add all three todos
    todo_page.add_todo(completed_todo_1)
    todo_page.add_todo(active_todo)
    todo_page.add_todo(completed_todo_2)

    # Verify all 3 todos exist
    expect(todo_page.todo_items).to_have_count(3)

    # ACT: Mark the first todo (index 0) as complete
    todo_page.mark_complete(0)

    # ACT: Mark the third todo (index 2) as complete
    # Note: After the first mark_complete, indices shift, but we mark index 2
    # which is now the third item (was index 2, still index 2)
    todo_page.mark_complete(2)

    # ASSERT: Verify count shows 1 item left (1 active, 2 completed)
    expect(todo_page.todo_count_label).to_contain_text("1")

    # ACT: Click the "Completed" filter
    todo_page.filter_by_completed()

    # ASSERT: Verify only 2 todos are visible (the completed ones)
    expect(todo_page.todo_items).to_have_count(2)

    # ASSERT: Verify both visible todos are the completed ones
    first_visible = todo_page.get_todo_by_index(0)
    second_visible = todo_page.get_todo_by_index(1)

    expect(first_visible.locator("label")).to_have_text(completed_todo_1)
    expect(second_visible.locator("label")).to_have_text(completed_todo_2)

    # ASSERT: Verify the active todo is NOT visible
    assert not todo_page.todo_exists(active_todo), (
        "Active todo should not appear in Completed filter"
    )

    # ACT: Switch back to "All" filter
    todo_page.filter_by_all()

    # ASSERT: Verify all 3 todos are visible again
    expect(todo_page.todo_items).to_have_count(3)


# =============================================================================
# TEST GROUP 5: Edge Cases and Additional Scenarios
# =============================================================================
# Additional tests to ensure robustness of the implementation
# =============================================================================


def test_add_multiple_todos_and_count(todo_page: TodoPage) -> None:
    """
    Test adding multiple todos and verifying the count updates correctly.

    This is an additional test to verify the counter works with multiple items.
    """
    # ARRANGE & ACT: Add 5 todos
    for i in range(1, 6):
        # Add a todo with a unique number
        todo_page.add_todo(f"Todo number {i}")

    # ASSERT: Verify 5 todos are in the list
    expect(todo_page.todo_items).to_have_count(5)

    # ASSERT: Verify count shows "5 items left"
    # The text should be "5 items left" (plural)
    expect(todo_page.todo_count_label).to_have_text("5 items left")


def test_complete_all_todos_empty_active_filter(todo_page: TodoPage) -> None:
    """
    Test that Active filter shows empty when all todos are completed.

    Edge case: When all items are complete, Active filter should show nothing.
    """
    # ARRANGE: Add two todos
    todo_page.add_todo("Task 1")
    todo_page.add_todo("Task 2")

    # ACT: Mark all as complete using the "toggle all" checkbox
    todo_page.mark_all_complete()

    # ASSERT: Verify count shows 0 items left
    expect(todo_page.todo_count_label).to_have_text("0 items left")

    # ACT: Switch to Active filter
    todo_page.filter_by_active()

    # ASSERT: No items should be visible
    expect(todo_page.todo_items).to_have_count(0)


def test_clear_completed_removes_completed_todos(todo_page: TodoPage) -> None:
    """
    Test that "Clear completed" button removes all completed todos.

    Edge case: Verify the clear functionality works correctly.
    """
    # ARRANGE: Add mixed todos
    todo_page.add_todo("Complete me")
    todo_page.add_todo("Keep me")

    # Mark first as complete
    todo_page.mark_complete(0)

    # ACT: Click "Clear completed" button
    todo_page.clear_completed()

    # ASSERT: Only 1 todo should remain
    expect(todo_page.todo_items).to_have_count(1)

    # ASSERT: The remaining todo should be "Keep me"
    remaining = todo_page.get_todo_by_index(0)
    expect(remaining.locator("label")).to_have_text("Keep me")
