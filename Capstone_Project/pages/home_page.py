"""
HomePage — Page Object for the automationexercise.com home page.
Handles navigation bar actions and header interactions.
"""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Represents the main landing page of automationexercise.com."""

    # ── Locators ───────────────────────────────────────────────────────────────
    LOGO               = (By.CSS_SELECTOR,  "div.logo img")
    SIGNUP_LOGIN_LINK  = (By.CSS_SELECTOR,  "a[href='/login']")
    LOGOUT_LINK        = (By.CSS_SELECTOR,  "a[href='/logout']")
    LOGGED_IN_AS_TEXT  = (By.XPATH,         "//a[contains(text(),'Logged in as')]")
    PRODUCTS_LINK      = (By.CSS_SELECTOR,  "a[href='/products']")
    CART_LINK          = (By.CSS_SELECTOR,  "a[href='/view_cart']")
    SEARCH_INPUT       = (By.CSS_SELECTOR,  "#search_product")
    SEARCH_BUTTON      = (By.CSS_SELECTOR,  "#submit_search")
    CONSENT_BUTTON     = (By.CSS_SELECTOR,  ".fc-button-label")   # cookie consent

    # ── Actions ────────────────────────────────────────────────────────────────

    def open_home(self):
        """Open the home page and dismiss any consent banners."""
        self.open(BASE_URL)
        self._dismiss_consent_if_present()
        logger.info("Home page opened.")

    def _dismiss_consent_if_present(self):
        """Click the cookie/consent button if it appears."""
        if self.is_element_present(*self.CONSENT_BUTTON):
            try:
                self.click(*self.CONSENT_BUTTON)
                logger.info("Cookie consent banner dismissed.")
            except Exception:
                pass  # not critical

    def is_home_page_loaded(self) -> bool:
        """Verify the logo and navbar are present."""
        return self.is_element_present(*self.LOGO)

    def navigate_to_login(self):
        """Click the Signup / Login link in the nav bar."""
        self.click(*self.SIGNUP_LOGIN_LINK)
        logger.info("Navigated to Login page.")

    def navigate_to_products(self):
        """Click the Products link in the nav bar."""
        self.click(*self.PRODUCTS_LINK)
        logger.info("Navigated to Products page.")

    def navigate_to_cart(self):
        """Click the Cart link in the nav bar."""
        self.click(*self.CART_LINK)
        logger.info("Navigated to Cart page.")

    def is_user_logged_in(self) -> bool:
        """Return True if 'Logged in as' text is visible in the nav."""
        return self.is_element_present(*self.LOGGED_IN_AS_TEXT)

    def get_logged_in_username(self) -> str:
        """Return the username displayed after login."""
        try:
            text = self.get_text(*self.LOGGED_IN_AS_TEXT)
            # text looks like: "Logged in as Test User"
            return text.replace("Logged in as", "").strip()
        except Exception:
            return ""

    def search_product(self, product_name: str):
        """
        Use the search bar on the home/products page to search for a product.
        NOTE: The search bar is on the Products page for automationexercise.com.
        Navigate there first if needed.
        """
        self.scroll_to_element(*self.SEARCH_INPUT)
        self.type_text(*self.SEARCH_INPUT, product_name)
        self.click(*self.SEARCH_BUTTON)
        logger.info(f"Searched for product: '{product_name}'")

    def logout(self):
        """Click the Logout link."""
        self.click(*self.LOGOUT_LINK)
        logger.info("Logged out.")
