"""
BasePage — Parent class for all Page Objects.
Provides reusable Selenium helper methods used across all page classes.
"""

import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)

from config.config import EXPLICIT_WAIT, SCREENSHOTS_DIR
from utils.screenshot_helper import capture_screenshot

logger = logging.getLogger(__name__)


class BasePage:
    """Base class inherited by every page object. Wraps Selenium interactions."""

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, EXPLICIT_WAIT)

    # ── Navigation ─────────────────────────────────────────────────────────────

    def open(self, url: str):
        """Navigate to a URL and log the action."""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    def get_title(self) -> str:
        """Return the current page title."""
        return self.driver.title

    def get_current_url(self) -> str:
        """Return the current URL."""
        return self.driver.current_url

    # ── Element Finders ────────────────────────────────────────────────────────

    def find_element(self, by: By, locator: str):
        """Wait for element to be present and return it."""
        try:
            element = self.wait.until(EC.presence_of_element_located((by, locator)))
            return element
        except TimeoutException:
            logger.error(f"Element not found: ({by}, {locator})")
            raise

    def find_visible_element(self, by: By, locator: str):
        """Wait for element to be visible and return it."""
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, locator)))
            return element
        except TimeoutException:
            logger.error(f"Element not visible: ({by}, {locator})")
            raise

    def find_clickable_element(self, by: By, locator: str):
        """Wait for element to be clickable and return it."""
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, locator)))
            return element
        except TimeoutException:
            logger.error(f"Element not clickable: ({by}, {locator})")
            raise

    def find_elements(self, by: By, locator: str):
        """Return a list of matching elements (may be empty)."""
        try:
            self.wait.until(EC.presence_of_all_elements_located((by, locator)))
        except TimeoutException:
            pass
        return self.driver.find_elements(by, locator)

    # ── Interactions ───────────────────────────────────────────────────────────

    def click(self, by: By, locator: str):
        """Click an element, using JS fallback if intercepted."""
        element = self.find_clickable_element(by, locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            logger.warning(f"Click intercepted for ({locator}), using JS click.")
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, by: By, locator: str, text: str, clear_first: bool = True):
        """Type text into an input field."""
        element = self.find_visible_element(by, locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"Typed '{text}' into ({locator})")

    def get_text(self, by: By, locator: str) -> str:
        """Return the visible text of an element."""
        return self.find_visible_element(by, locator).text.strip()

    def get_attribute(self, by: By, locator: str, attribute: str) -> str:
        """Return a specific attribute value of an element."""
        return self.find_element(by, locator).get_attribute(attribute)

    # ── Waits ──────────────────────────────────────────────────────────────────

    def wait_for_url_contains(self, partial_url: str, timeout: int = EXPLICIT_WAIT):
        """Wait until the current URL contains the given substring."""
        WebDriverWait(self.driver, timeout).until(EC.url_contains(partial_url))

    def wait_for_element_visible(self, by: By, locator: str, timeout: int = EXPLICIT_WAIT):
        """Wait until the element becomes visible."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )

    def wait_for_element_invisible(self, by: By, locator: str, timeout: int = EXPLICIT_WAIT):
        """Wait until an element disappears from view."""
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((by, locator))
        )

    def is_element_present(self, by: By, locator: str) -> bool:
        """Return True if the element exists in the DOM."""
        try:
            self.driver.find_element(by, locator)
            return True
        except NoSuchElementException:
            return False

    # ── JavaScript Helpers ─────────────────────────────────────────────────────

    def scroll_to_element(self, by: By, locator: str):
        """Scroll the element into view."""
        element = self.find_element(by, locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.4)

    def scroll_to_top(self):
        """Scroll to the top of the page."""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # ── Alert / Popup Handling ─────────────────────────────────────────────────

    def handle_alert(self, action: str = "accept") -> str:
        """
        Handle a JavaScript alert/confirm/prompt.
        :param action: 'accept' or 'dismiss'
        :return: Alert text before handling
        """
        try:
            alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            text  = alert.text
            logger.info(f"Alert detected with text: '{text}'")
            if action == "accept":
                alert.accept()
            else:
                alert.dismiss()
            logger.info(f"Alert {action}ed.")
            return text
        except TimeoutException:
            logger.info("No JS alert present.")
            return ""

    def is_alert_present(self) -> bool:
        """Return True if a JS alert is currently visible."""
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            return True
        except TimeoutException:
            return False

    # ── Screenshot ─────────────────────────────────────────────────────────────

    def screenshot(self, step_name: str) -> str:
        """Capture and save a screenshot; return the saved file path."""
        path = capture_screenshot(self.driver, step_name)
        logger.info(f"Screenshot saved: {path}")
        return path
