"""
LoginPage — Page Object for the automationexercise.com login page.
Handles login form submission and verification.
"""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import LOGIN_URL

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Represents the Login/Signup page at /login."""

    # ── Locators ───────────────────────────────────────────────────────────────
    LOGIN_EMAIL_INPUT    = (By.CSS_SELECTOR,  "input[data-qa='login-email']")
    LOGIN_PASSWORD_INPUT = (By.CSS_SELECTOR,  "input[data-qa='login-password']")
    LOGIN_BUTTON         = (By.CSS_SELECTOR,  "button[data-qa='login-button']")
    LOGIN_HEADING        = (By.XPATH,         "//h2[text()='Login to your account']")
    ERROR_MESSAGE        = (By.CSS_SELECTOR,  "p[style='color: red;']")
    LOGGED_IN_AS_TEXT    = (By.XPATH,         "//a[contains(text(),'Logged in as')]")

    # ── Actions ────────────────────────────────────────────────────────────────

    def open_login_page(self):
        """Open the login URL directly."""
        self.open(LOGIN_URL)
        self.find_visible_element(*self.LOGIN_HEADING)
        logger.info("Login page opened and heading verified.")

    def is_login_page_loaded(self) -> bool:
        """Return True if the login heading is visible."""
        return self.is_element_present(*self.LOGIN_HEADING)

    def enter_email(self, email: str):
        """Type email into the login email field."""
        self.type_text(*self.LOGIN_EMAIL_INPUT, email)

    def enter_password(self, password: str):
        """Type password into the login password field."""
        self.type_text(*self.LOGIN_PASSWORD_INPUT, password)

    def click_login_button(self):
        """Click the Login button."""
        self.click(*self.LOGIN_BUTTON)
        logger.info("Login button clicked.")

    def login(self, email: str, password: str):
        """
        Full login sequence:
        1. Enter email
        2. Enter password
        3. Click login
        """
        logger.info(f"Attempting login with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.screenshot("02_login_credentials_entered")
        self.click_login_button()

    def is_login_successful(self) -> bool:
        """
        Return True if the 'Logged in as' text appears in the nav bar
        after login (indicates successful authentication).
        """
        return self.is_element_present(*self.LOGGED_IN_AS_TEXT)

    def get_error_message(self) -> str:
        """Return the error message text if login fails."""
        if self.is_element_present(*self.ERROR_MESSAGE):
            return self.get_text(*self.ERROR_MESSAGE)
        return ""
