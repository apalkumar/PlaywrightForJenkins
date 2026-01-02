import pytest
from pathlib import Path
from utilities.excel_register import get_excel_data
from pages.login_page import Loginpage
from playwright.sync_api import Playwright

# directories
VIDEO_DIR = Path("test-results/videos")
SCREENSHOT_DIR = Path("test-results/screenshots")

# load excel data once
test_data = get_excel_data("test_data.xlsx", "Sheet1")


# ------------------------
# Browser / Page Fixtures
# ------------------------

@pytest.fixture(scope="function")
def browser_context(playwright: Playwright):
    """
    Each test gets a fresh browser context
    safe for pytest-xdist parallel runs.
    """
    browser = playwright.chromium.launch(headless=False)

    context = browser.new_context(
        viewport=None,
        record_video_dir=str(VIDEO_DIR),
        record_video_size={"width": 1920, "height": 1080},
    )

    yield context

    context.close()
    browser.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """
    New page for each test
    """
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def logged_in_page(page):
    """
    Logs in before register test.
    """
    login_data = test_data[0]
    login = Loginpage(page)
    login.open(login_data["Url"])
    login.enter_initial_email(login_data["Email"])
    return page


# ------------------------
# pytest-html Screenshot Hook
# ------------------------

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # ------- Screenshot on failure --------
    if report.when == "call" and report.failed and "page" in item.funcargs:
        page_obj = item.funcargs["page"]

        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_file = SCREENSHOT_DIR / f"{item.name}_{report.nodeid.replace('::','_')}.png"

        page_obj.screenshot(path=str(screenshot_file))

        extra = getattr(report, "extra", [])
        extra.append(pytest_html.extras.image(str(screenshot_file), mime_type="image/png"))
        report.extra = extra

    # ------- Video cleanup --------
    video_file = VIDEO_DIR / f"{item.name}_{report.nodeid.replace('::','_')}.webm"

    if report.when == "call":
        # delete passing videos
        if report.passed and video_file.exists():
            video_file.unlink()
