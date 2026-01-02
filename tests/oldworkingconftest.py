import pytest
from pathlib import Path
from playwright.sync_api import Playwright
import tkinter as tk

VIDEO_DIR = Path("test_results/videos")
SCREENSHOT_DIR = Path("test_results/screenshots")

# root = tk.Tk()
# screenwidth = root.winfo_screenwidth
# screenheight = root.winfo_screenheight

@pytest.fixture(scope='session')
def browser_context(playwright: Playwright):
    browser = playwright.chromium.launch(
        headless=False
        # args=["--start-maximized", "--window-size=1920,1080"]
    )

    context = browser.new_context(
        viewport=None,
        record_video_dir=str(VIDEO_DIR),
        record_video_size={"width": 1920, "height": 1080},
    )

    yield context
    context.close()
    browser.close()

@pytest.fixture(scope='session')
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

# pytest-html plugin object
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # screenshot on failure
    if report.when == "call" and report.failed and "page" in item.funcargs:
        page = item.funcargs["page"]
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_file = SCREENSHOT_DIR / f"{item.name}.png"
        page.screenshot(path=str(screenshot_file))
        extra = getattr(report, "extra", [])
        extra.append(pytest_html.extras.image(str(screenshot_file), mime_type="image/png"))
        report.extra = extra

    # video cleanup
    video_file = VIDEO_DIR / f"{item.name}.webm"
    if report.when == "call":
        if report.passed and video_file.exists():
            video_file.unlink()
