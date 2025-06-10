from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="Run headless")
    parser.addoption("--resolution", action="store", default="1280x720", help="Viewport WxH")


def pytest_configure(config):
    root_dir = Path(__file__).parent.resolve()  # or customize for your actual root
    report_path = root_dir / "reports" / "report.html"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    config.option.htmlpath = str(report_path)


@pytest.fixture(scope="session")
def browser_name(request) -> str:
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def browser_type_launch_args(request):
    return {
        "headless": request.config.getoption("--headless")
    }


@pytest.fixture(scope="function")
def browser_context_args(request):
    width, height = map(int, request.config.getoption("--resolution").split("x"))
    return {
        "viewport": {"width": width, "height": height}
    }


@pytest.fixture(scope="session")
def browser_type(playwright, browser_name):
    return getattr(playwright, browser_name)


@pytest.fixture(scope="session")
def browser(browser_type, browser_type_launch_args):
    browser = browser_type.launch(**browser_type_launch_args)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser, browser_context_args):
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(autouse=True)
def page(context):
    page = context.new_page()
    yield page
    page.close()
