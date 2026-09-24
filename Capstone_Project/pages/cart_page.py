"""
CartPage — Page Object for the automationexercise.com cart page.
Handles cart verification: product name, quantity, price, and totals.
"""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import CART_URL

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Represents the shopping cart at /view_cart."""

    # ── Locators ───────────────────────────────────────────────────────────────
    CART_TABLE           = (By.CSS_SELECTOR, "#cart_info_table")
    CART_ROWS            = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    CART_PRODUCT_NAMES   = (By.CSS_SELECTOR, ".cart_description h4 a")
    CART_PRICES          = (By.CSS_SELECTOR, ".cart_price p")
    CART_QUANTITIES      = (By.CSS_SELECTOR, ".cart_quantity button")
    CART_TOTALS          = (By.CSS_SELECTOR, ".cart_total p.cart_total_price")
    PROCEED_CHECKOUT_BTN = (By.CSS_SELECTOR, ".check_out")
    EMPTY_CART_MSG       = (By.CSS_SELECTOR, "#empty_cart b")

    # ── Actions ────────────────────────────────────────────────────────────────

    def open_cart(self):
        """Navigate directly to the cart page and wait for content to render."""
        from selenium.webdriver.support.ui import WebDriverWait
        self.open(CART_URL)
        # Wait for cart content to be ready — either rows or empty-cart message.
        # Required because automationexercise.com populates cart via JavaScript,
        # and Firefox eager loading marks the page ready before JS runs.
        try:
            WebDriverWait(self.driver, 15).until(
                lambda d: (
                    d.find_elements(By.CSS_SELECTOR, "#cart_info_table tbody tr") or
                    d.find_elements(By.CSS_SELECTOR, "#empty_cart")
                )
            )
        except Exception:
            pass  # Proceed anyway; actual emptiness check is done per test
        logger.info("Cart page opened.")

    def is_cart_empty(self) -> bool:
        """Return True if the cart has no item rows (more reliable than message check)."""
        rows = self.find_elements(*self.CART_ROWS)
        if len(rows) > 0:
            return False
        # Fall back to the empty-cart banner as secondary confirmation
        return self.is_element_present(*self.EMPTY_CART_MSG)

    def get_cart_item_count(self) -> int:
        """Return the number of product rows in the cart."""
        rows = self.find_elements(*self.CART_ROWS)
        count = len(rows)
        logger.info(f"Cart item count: {count}")
        return count

    def get_product_names_in_cart(self) -> list[str]:
        """Return a list of product names currently in the cart."""
        elements = self.find_elements(*self.CART_PRODUCT_NAMES)
        names = [el.text.strip() for el in elements]
        logger.info(f"Products in cart: {names}")
        return names

    def get_quantities_in_cart(self) -> list[str]:
        """Return a list of quantity values (as strings) for each cart row."""
        elements = self.find_elements(*self.CART_QUANTITIES)
        quantities = [el.text.strip() for el in elements]
        logger.info(f"Cart quantities: {quantities}")
        return quantities

    def get_prices_in_cart(self) -> list[str]:
        """Return a list of unit price strings for each cart row."""
        elements = self.find_elements(*self.CART_PRICES)
        prices = [el.text.strip() for el in elements]
        logger.info(f"Cart prices: {prices}")
        return prices

    def get_totals_in_cart(self) -> list[str]:
        """Return a list of row-total price strings."""
        elements = self.find_elements(*self.CART_TOTALS)
        totals = [el.text.strip() for el in elements]
        logger.info(f"Cart totals: {totals}")
        return totals

    def get_cart_summary(self) -> dict:
        """
        Return a dictionary summarising the full cart state:
        {
            'item_count': int,
            'product_names': [str],
            'quantities': [str],
            'prices': [str],
            'totals': [str],
        }
        """
        summary = {
            "item_count":    self.get_cart_item_count(),
            "product_names": self.get_product_names_in_cart(),
            "quantities":    self.get_quantities_in_cart(),
            "prices":        self.get_prices_in_cart(),
            "totals":        self.get_totals_in_cart(),
        }
        logger.info(f"Cart summary: {summary}")
        return summary

    def is_product_in_cart(self, product_name: str) -> bool:
        """Return True if the product name is found in the cart (case-insensitive)."""
        names = self.get_product_names_in_cart()
        return any(product_name.lower() in n.lower() for n in names)

    def get_quantity_for_product(self, product_name: str) -> str:
        """Return the quantity string for a specific product in the cart."""
        rows = self.find_elements(*self.CART_ROWS)
        for row in rows:
            try:
                name_el = row.find_element(By.CSS_SELECTOR, ".cart_description h4 a")
                if product_name.lower() in name_el.text.strip().lower():
                    qty_el = row.find_element(By.CSS_SELECTOR, ".cart_quantity button")
                    return qty_el.text.strip()
            except Exception:
                continue
        return ""

    def proceed_to_checkout(self):
        """Click the 'Proceed To Checkout' button."""
        self.scroll_to_element(*self.PROCEED_CHECKOUT_BTN)
        self.click(*self.PROCEED_CHECKOUT_BTN)
        logger.info("Clicked 'Proceed To Checkout'.")
