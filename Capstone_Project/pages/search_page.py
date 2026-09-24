"""
SearchPage — Page Object for the automationexercise.com products/search page.
Handles product searching and result selection.
"""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import PRODUCTS_URL

logger = logging.getLogger(__name__)


class SearchPage(BasePage):
    """Represents the /products page and search results listing."""

    # ── Locators ───────────────────────────────────────────────────────────────
    SEARCH_INPUT       = (By.CSS_SELECTOR, "#search_product")
    SEARCH_BUTTON      = (By.CSS_SELECTOR, "#submit_search")
    SEARCH_HEADING     = (By.CSS_SELECTOR, "h2.title.text-center")
    SEARCHED_PRODUCTS  = (By.CSS_SELECTOR, ".productinfo.text-center")
    # NOTE: On automationexercise.com the product PRICE is in <h2> and
    #       the product NAME is in <p> inside .productinfo.text-center
    PRODUCT_NAMES      = (By.CSS_SELECTOR, ".productinfo.text-center p")
    ALL_PRODUCT_CARDS  = (By.CSS_SELECTOR, ".features_items .col-sm-4")
    VIEW_PRODUCT_LINKS = (By.CSS_SELECTOR, "a[href*='product_details']")
    NO_RESULT_TEXT     = (By.CSS_SELECTOR, "#search_product_results .features_items")

    # ── Actions ────────────────────────────────────────────────────────────────

    def open_products_page(self):
        """Navigate directly to the products listing page."""
        self.open(PRODUCTS_URL)
        logger.info("Products page opened.")

    def search_for(self, product_name: str):
        """Enter a product name in the search box and submit."""
        self.scroll_to_element(*self.SEARCH_INPUT)
        self.type_text(*self.SEARCH_INPUT, product_name)
        self.screenshot("03a_search_term_entered")
        self.click(*self.SEARCH_BUTTON)
        logger.info(f"Search submitted for: '{product_name}'")
        # Explicitly wait for product name elements to appear in the DOM.
        # Needed because automationexercise.com renders results via JavaScript
        # and Firefox eager loading considers the page ready before JS runs.
        try:
            self.wait_for_element_visible(*self.PRODUCT_NAMES)
        except Exception:
            pass  # Will be caught by assertion in the test
        self.screenshot("03b_search_results")

    def get_search_result_names(self) -> list[str]:
        """Return a list of product names from the search results."""
        elements = self.find_elements(*self.PRODUCT_NAMES)
        names = [el.text.strip() for el in elements]
        logger.info(f"Search results found: {names}")
        return names

    def get_result_count(self) -> int:
        """Return the number of products shown in search results."""
        elements = self.find_elements(*self.SEARCHED_PRODUCTS)
        return len(elements)

    def is_product_in_results(self, product_name: str) -> bool:
        """Return True if the product name appears in search results (case-insensitive)."""
        names = self.get_search_result_names()
        return any(product_name.lower() in n.lower() for n in names)

    def click_view_product(self, product_name: str):
        """
        Find the product card matching the name and click 'View Product'.
        Scrolls to the product card before clicking.
        """
        cards = self.find_elements(*self.ALL_PRODUCT_CARDS)
        for card in cards:
            try:
                name_el = card.find_element(By.CSS_SELECTOR, ".productinfo.text-center p")
                if product_name.lower() in name_el.text.strip().lower():
                    view_link = card.find_element(By.CSS_SELECTOR, "a[href*='product_details']")
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});", view_link
                    )
                    self.driver.execute_script("arguments[0].click();", view_link)
                    logger.info(f"Clicked 'View Product' for: '{product_name}'")
                    return
            except Exception:
                continue

        # Fallback: click the first available view link
        links = self.find_elements(*self.VIEW_PRODUCT_LINKS)
        if links:
            self.driver.execute_script("arguments[0].click();", links[0])
            logger.warning(f"Exact product '{product_name}' not matched; clicked first result.")
        else:
            raise AssertionError(f"No 'View Product' link found for '{product_name}'")
