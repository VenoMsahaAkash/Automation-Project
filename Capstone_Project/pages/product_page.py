"""
ProductPage — Page Object for the automationexercise.com product detail page.
Handles quantity setting, adding to cart, and modal popup interactions.
"""

import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from config.config import EXPLICIT_WAIT

logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    """Represents the product detail page at /product_details/<id>."""

    # ── Locators ───────────────────────────────────────────────────────────────
    PRODUCT_NAME      = (By.CSS_SELECTOR, ".product-information h2")
    PRODUCT_PRICE     = (By.CSS_SELECTOR, ".product-information span span")
    PRODUCT_CATEGORY  = (By.CSS_SELECTOR, ".product-information p:nth-child(3)")
    QUANTITY_INPUT    = (By.CSS_SELECTOR, "#quantity")
    ADD_TO_CART_BTN   = (By.CSS_SELECTOR, ".cart")

    # Modal popup after adding to cart
    MODAL             = (By.CSS_SELECTOR, "#cartModal")
    MODAL_TITLE       = (By.CSS_SELECTOR, "#cartModal .modal-title")
    MODAL_CONTINUE    = (By.CSS_SELECTOR, "#cartModal button.close-modal, "
                                          "#cartModal .btn-success")
    MODAL_VIEW_CART   = (By.CSS_SELECTOR, "#cartModal a[href='/view_cart']")

    # ── Actions ────────────────────────────────────────────────────────────────

    def get_product_name(self) -> str:
        """Return the product name displayed on the detail page."""
        return self.get_text(*self.PRODUCT_NAME)

    def get_product_price(self) -> str:
        """Return the product price string (e.g., 'Rs. 500')."""
        return self.get_text(*self.PRODUCT_PRICE)

    def set_quantity(self, quantity: int):
        """
        Clear the quantity field and enter the desired quantity.
        :param quantity: Integer quantity to set (e.g., 2)
        """
        self.scroll_to_element(*self.QUANTITY_INPUT)
        qty_input = self.find_visible_element(*self.QUANTITY_INPUT)
        qty_input.clear()
        qty_input.send_keys(str(quantity))
        logger.info(f"Quantity set to: {quantity}")

    def click_add_to_cart(self):
        """Click the 'Add to Cart' button on the product detail page."""
        self.scroll_to_element(*self.ADD_TO_CART_BTN)
        self.click(*self.ADD_TO_CART_BTN)
        logger.info("'Add to Cart' button clicked.")

    def wait_for_modal(self) -> bool:
        """
        Wait for the 'Added to Cart' modal popup to appear.
        :return: True if modal appeared, False if it timed out.
        """
        try:
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.visibility_of_element_located(self.MODAL)
            )
            logger.info("Cart confirmation modal is visible.")
            return True
        except Exception:
            logger.warning("Cart modal did not appear within timeout.")
            return False

    def get_modal_title(self) -> str:
        """Return the title text of the cart modal."""
        try:
            return self.get_text(*self.MODAL_TITLE)
        except Exception:
            return ""

    def click_continue_shopping(self):
        """Click the 'Continue Shopping' button to close the modal."""
        self.click(*self.MODAL_CONTINUE)
        self.wait_for_element_invisible(*self.MODAL)
        logger.info("Clicked 'Continue Shopping' — modal closed.")

    def click_view_cart_in_modal(self):
        """Click the 'View Cart' link inside the cart modal."""
        self.click(*self.MODAL_VIEW_CART)
        logger.info("Clicked 'View Cart' in modal — navigating to cart.")

    def add_product_to_cart(self, quantity: int = 1):
        """
        High-level method: set quantity, add to cart, wait for modal.
        :param quantity: Desired quantity.
        :return: True if modal confirmed success.
        """
        self.set_quantity(quantity)
        self.screenshot("04a_quantity_set")
        self.click_add_to_cart()
        time.sleep(0.5)  # brief pause before modal check
        modal_visible = self.wait_for_modal()
        self.screenshot("04b_cart_modal")
        return modal_visible
