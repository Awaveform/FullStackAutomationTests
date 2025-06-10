from pathlib import Path
from typing import Any, Dict, Generator

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from _pytest.nodes import Item
from playwright.sync_api import (
    Browser, BrowserType, BrowserContext, Page, Playwright
)

PROJECT_ROOT = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_ROOT / "reports"
VIDEOS_DIR = REPORTS_DIR / "videos"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser: Parser) -> None:
    """
    Adds custom CLI options for headless mode and viewport resolution.

    :param parser: Pytest parser object
    """

    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Run headless"
    )
    parser.addoption(
        "--resolution", action="store", default="1280x720",
        help="Viewport WxH"
    )


def pytest_configure(config: Config) -> None:
    """
    Configures the default report output path to be under /reports/report.html.

    :param config: Pytest config object
    """

    root_dir = Path(__file__).parent.resolve()
    report_path = root_dir / "reports" / "report.html"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    config.option.htmlpath = str(report_path)


@pytest.fixture(scope="session")
def browser_name(request: SubRequest) -> str:
    """
    Returns the selected browser type via --browser CLI option.

    :param request: Pytest request object
    :return: Browser name as string
    """

    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def browser_type_launch_args(request: SubRequest) -> Dict[str, bool]:
    """
    Constructs launch arguments for the browser instance.

    :param request: Pytest request object
    :return: Dictionary with Playwright launch args
    """

    return {
        "headless": request.config.getoption("--headless")
    }


@pytest.fixture(scope="function")
def browser_context_args(request: SubRequest) -> Dict[str, Any]:
    """
    Prepares context configuration, including viewport and video recording dir.

    :param request: Pytest request object
    :return: Dictionary with context creation args
    """

    width, height = map(
        int, request.config.getoption("--resolution").split("x")
    )
    video_dir = Path(__file__).resolve().parent / "reports" / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)
    return {
        "viewport": {"width": width, "height": height},
        "record_video_dir": video_dir
    }


@pytest.fixture(scope="session")
def browser_type(playwright: Playwright, browser_name: str) -> BrowserType:
    """
    Retrieves browser type object from Playwright using CLI option.

    :param playwright: Playwright instance
    :param browser_name: String name of a browser type
    :return: object (chromium, firefox, webkit)
    """

    return getattr(playwright, browser_name)


@pytest.fixture(scope="session")
def browser(
        browser_type: BrowserType,
        browser_type_launch_args: Dict[str, bool]
) -> Generator[Browser, Any, None]:
    """
    Launches a browser instance for the test session.

    :param browser_type: Browser type object
    :param browser_type_launch_args: Launch arguments dict
    :yield: Playwright browser instance
    """

    browser = browser_type.launch(**browser_type_launch_args)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(
        browser: Browser,
        browser_context_args: Dict[str, Any],
        request: SubRequest,
        page: Page
) -> Generator[BrowserContext, Any, None]:
    """
    Creates a new browser context for each test function,
    saves video if available after test.

    :param browser: Browser instance
    :param browser_context_args: Dict with viewport and recording config
    :param request: Pytest request object
    :param page: Page fixture (required to bind context pages)
    :yield: Browser context
    """

    context = browser.new_context(**browser_context_args)
    yield context

    # save video after context is closed
    context.close()

    for page in context.pages:
        video = page.video
        if video:
            video_path = video.path()
            if video_path and Path(video_path).exists():
                final_path = REPORTS_DIR / f"{request.node.name}.webm"
                Path(video_path).rename(final_path)


@pytest.fixture(autouse=True)
def page(context: BrowserContext, request: SubRequest) -> (
        Generator)[Page, Any, None]:
    """
    Automatically provides a new page for each test.
    Captures a screenshot if the test fails.

    :param context: Browser context
    :param request: Pytest request object
    :yield: Page object
    """

    page = context.new_page()

    yield page

    # screenshot on failure
    if request.node.rep_call.failed:
        screenshot_path = REPORTS_DIR / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: Any) -> Any:
    """
    Pytest hook to attach a test result (rep_setup/rep_call/rep_teardown)
    to the test item for later access.

    :param item: Test function item
    :param call: Call phase
    """

    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
