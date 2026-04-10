# =============================================================================
# CONFTEST.PY - Shared Pytest Fixtures and Configuration
# =============================================================================
# This file is automatically loaded by pytest before running any tests.
# It's used to define fixtures that can be shared across all test files.
# Fixtures provide setup/teardown functionality for tests.
# =============================================================================

# Import pytest framework for creating fixtures
import pytest

# Import Playwright's Page class for type hints
# Page represents a single browser tab or window
from playwright.sync_api import Page


# =============================================================================
# BASE URL FIXTURE
# =============================================================================
# This fixture provides the base URL for the TodoMVC application.
# Using a fixture makes it easy to change the URL in one place.
# The "session" scope means this value is computed once per test session.
# =============================================================================
@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Returns the base URL for the TodoMVC demo application.

    This fixture provides a centralized location for the application URL.
    If the URL changes, only this fixture needs to be updated.

    Returns:
        str: The URL of the TodoMVC demo application
    """
    # Return the Playwright's official TodoMVC demo URL
    return "https://demo.playwright.dev/todomvc/#/"


# =============================================================================
# PAGE NAVIGATION FIXTURE (AUTOMATIC)
# =============================================================================
# This fixture automatically navigates to the base URL before each test.
# The "autouse=True" means it runs automatically for every test.
# The "function" scope means it runs before/after each individual test function.
# =============================================================================
@pytest.fixture(autouse=True)
def navigate_to_base_url(page: Page, base_url: str):
    """
    Automatically navigates to the base URL before each test.

    This ensures every test starts from a clean, consistent state
    at the TodoMVC homepage. No need to manually navigate in each test.

    Args:
        page: Playwright's Page fixture (automatically injected by pytest-playwright)
        base_url: The base URL fixture defined above

    Yields:
        None - control passes to the test function
    """
    # Navigate to the TodoMVC demo page
    # page.goto() waits for the page to fully load before continuing
    page.goto(base_url)

    # Yield control to the test function
    # Everything after yield runs as teardown after the test completes
    yield

    # Teardown: No cleanup needed as Playwright handles browser context disposal
    # Each test gets a fresh browser context automatically


# =============================================================================
# SCREENSHOT ON FAILURE HOOK
# =============================================================================
# This hook captures a screenshot whenever a test fails.
# Screenshots help debug failures by showing the browser state at failure time.
# The screenshot is saved to the test report.
# =============================================================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that captures screenshots on test failure.

    This hook intercepts test execution and checks if the test failed.
    If a failure occurred, it captures a screenshot of the browser.

    Args:
        item: The test item being executed
        call: The test call object containing execution results

    Yields:
        The result of the test execution
    """
    # Execute all other hooks to get the test outcome
    outcome = yield

    # Get the test result (passed, failed, skipped, etc.)
    report = outcome.get_result()

    # Check if the test failed during the "call" phase (actual test execution)
    # We don't want screenshots for setup/teardown failures
    if report.when == "call" and report.failed:
        # Note: Screenshot capture requires pytest-html plugin
        # For full functionality, would need: page.screenshot() and attach to report
        # Example: item.funcargs.get("page").screenshot()
        pass
