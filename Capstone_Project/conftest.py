"""
conftest.py — pytest configuration and shared fixtures.

Provides:
- A session-scoped WebDriver fixture (Chrome by default)
- Automatic screenshot-on-failure hook
- Teardown (browser close)
"""

import os
import logging
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config.config import (
    BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT,
    SCREENSHOTS_DIR, REPORTS_DIR,
)
from utils.screenshot_helper import capture_screenshot

logger = logging.getLogger(__name__)

# ─── Ensure output directories exist ─────────────────────────────────────────
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


# ─── WebDriver Fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def driver():
    """
    Session-scoped Selenium WebDriver fixture.
    The same browser instance is shared across all tests in the session.
    Teardown closes the browser after all tests have run.
    """
    browser = BROWSER.lower()
    logger.info(f"Launching browser: {browser.upper()} | Headless: {HEADLESS}")

    drv = _create_driver(browser)
    drv.implicitly_wait(IMPLICIT_WAIT)
    drv.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    drv.maximize_window()

    yield drv

    logger.info("Closing browser after test session.")
    drv.quit()


def _create_driver(browser: str):
    """Factory function to create the correct WebDriver instance."""
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if HEADLESS:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        # 'eager' = don't wait for ads/images, proceed when DOM is interactive
        options.page_load_strategy = "eager"
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("permissions.default.image", 1)
        if HEADLESS:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: '{browser}'. Choose 'chrome' or 'firefox'.")


# ─── Screenshot-on-Failure Hook ───────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    After each test, if it FAILED, capture a screenshot automatically
    and attach it to the pytest-html report.
    """
    outcome = yield
    report  = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture:
            step_name  = f"FAILED_{item.name}"
            screenshot = capture_screenshot(driver_fixture, step_name)
            logger.error(f"Test FAILED — screenshot: {screenshot}")

            # Attach screenshot to pytest-html report
            if hasattr(report, "extra"):
                from pytest_html import extras
                report.extra = getattr(report, "extra", [])
                report.extra.append(extras.image(screenshot))


# ─── pytest-html Report Title ─────────────────────────────────────────────────

def pytest_html_report_title(report):
    """Set a custom title for the HTML execution report."""
    report.title = "Capstone Project — E-Commerce Automation Report"
