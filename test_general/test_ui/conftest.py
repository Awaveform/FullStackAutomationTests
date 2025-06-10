from pathlib import Path
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from _pytest.nodes import Item
from playwright.sync_api import (
    Playwright,
    BrowserType,
    Browser,
    BrowserContext,
    Page, ViewportSize
)

from pages.upload_page import UploadPage
from utilities.env_settings import env_settings

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
VIDEOS_DIR: Path = REPORTS_DIR / "videos"

VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def browser_type(playwright: Playwright) -> BrowserType:
    """
    Returns the default browser type (chromium).

    :param playwright: Playwright instance
    :return: BrowserType instance
    """

    return playwright.chromium


@pytest.fixture(scope="session")
def browser(browser_type: BrowserType) -> Generator[Browser, None, None]:
    """
    Launches and yields a browser instance.

    :param browser_type: Selected browser type
    :yield: Browser instance
    """

    browser = browser_type.launch(
        headless=env_settings.HEADLESS,
        timeout=int(env_settings.PLAYWRIGHT_TIMEOUT),
        slow_mo=int(env_settings.PLAYWRIGHT_SLOWMO)
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Creates a new browser context for each test function.

    :param browser: Browser instance
    :yield: BrowserContext
    """

    context = browser.new_context(
        viewport=ViewportSize(width=1280, height=720),
        record_video_dir=VIDEOS_DIR
    )
    yield context
    context.close()


@pytest.fixture(scope="function", autouse=True)
def page(
        context: BrowserContext,
        request: SubRequest
) -> Generator[Page, None, None]:
    """
    Creates a new page for each test. Captures screenshot on failure.

    :param context: BrowserContext instance
    :param request: SubRequest object
    :yield: Page instance
    """

    page = context.new_page()
    yield page

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_path = REPORTS_DIR / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item) -> Generator[None, None, None]:
    """
    Hook to attach test phase results (setup/call/teardown) to the test item.

    :param item: Test item object
    :yield: None
    """

    outcome = yield
    # noinspection PyUnresolvedReferences
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def upload_page(page: Page) -> UploadPage:
    """
    Returns a Page Object for the UploadPage.

    :param page: Page fixture instance
    :return: UploadPage object
    """

    return UploadPage(page)
