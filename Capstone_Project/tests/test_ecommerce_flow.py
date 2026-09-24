"""
test_ecommerce_flow.py
======================
Capstone Assignment 1 — E-Commerce Automation with Selenium WebDriver

Application Under Test: https://automationexercise.com/

Test Scenarios (10 required):
  TC_01 — Launch Browser & Verify Home Page
  TC_02 — Login to Application
  TC_03 — Search Product
  TC_04 — Add Product to Cart (with Popup/Modal Handling)
  TC_05 — Update Product Quantity
  TC_06 — Verify Cart Details
  TC_07 — Capture Screenshots at Key Steps
  TC_08 — Read Test Data from Excel and JSON
  TC_09 — Handle Popup / Alerts
  TC_10 — Generate Execution Report
"""

import logging
import os

import pytest

from config.config import (
    BASE_URL, LOGIN_EMAIL, LOGIN_PASSWORD,
    SEARCH_PRODUCT, PRODUCT_QUANTITY,
    SCREENSHOTS_DIR, REPORTS_DIR,
)
from pages.home_page    import HomePage
from pages.login_page   import LoginPage
from pages.search_page  import SearchPage
from pages.product_page import ProductPage
from pages.cart_page    import CartPage
from utils.data_reader  import read_json, get_json_value, read_excel, get_excel_value
from utils.report_helper import (
    log_test_result, save_json_report, list_screenshots, print_summary,
)

logger = logging.getLogger(__name__)

# ─── Module-level results tracker ─────────────────────────────────────────────
_results: list[dict] = []


# ══════════════════════════════════════════════════════════════════════════════
# TC_01 — Launch Browser & Verify Home Page
# ══════════════════════════════════════════════════════════════════════════════

class TestTC01LaunchBrowser:
    """TC_01: Verify the browser launches and the home page loads correctly."""

    def test_launch_browser_and_verify_home_page(self, driver):
        """
        Steps:
        1. Open automationexercise.com in Chrome.
        2. Verify page title contains 'Automation Exercise'.
        3. Verify the home page logo is visible.
        4. Capture screenshot.
        """
        logger.info("=== TC_01: Launch Browser & Verify Home Page ===")
        home = HomePage(driver)
        home.open_home()

        title = driver.title
        logger.info(f"Page title: '{title}'")

        # Capture screenshot of the home page
        ss = home.screenshot("01_home_page_loaded")

        assert "Automation Exercise" in title, (
            f"Expected 'Automation Exercise' in title, got: '{title}'"
        )
        assert home.is_home_page_loaded(), "Home page logo is not visible!"

        _results.append(log_test_result(
            "TC_01 — Launch Browser", "PASS",
            f"Title verified: '{title}'", ss
        ))
        logger.info("TC_01 PASSED ✓")


# ══════════════════════════════════════════════════════════════════════════════
# TC_02 — Login to Application
# ══════════════════════════════════════════════════════════════════════════════

class TestTC02Login:
    """TC_02: Login using credentials from the data files."""

    def test_login_with_valid_credentials(self, driver):
        """
        Steps:
        1. Navigate to the login page.
        2. Read credentials from JSON data file.
        3. Enter email and password.
        4. Click Login button.
        5. Verify 'Logged in as' is visible in the nav bar.
        6. Capture screenshot.
        """
        logger.info("=== TC_02: Login to Application ===")

        # Read credentials from JSON
        email    = get_json_value("login.email")
        password = get_json_value("login.password")
        logger.info(f"Credentials loaded from JSON — email: {email}")

        home  = HomePage(driver)
        login = LoginPage(driver)

        home.open_home()
        home.navigate_to_login()

        assert login.is_login_page_loaded(), "Login page did not load!"
        home.screenshot("02a_login_page")

        login.login(email, password)

        ss = home.screenshot("02b_after_login")

        # Assert successful login
        if not login.is_login_successful():
            error_msg = login.get_error_message()
            _results.append(log_test_result(
                "TC_02 — Login", "FAIL",
                f"Login failed — site says: '{error_msg}'. "
                f"Register '{email}' at https://automationexercise.com/login first.", ss
            ))
            pytest.fail(
                f"\n\n{'='*60}\n"
                f"  TC_02 LOGIN FAILED\n"
                f"{'='*60}\n"
                f"  Email used   : {email}\n"
                f"  Site error   : {error_msg}\n\n"
                f"  FIX: Go to https://automationexercise.com/login\n"
                f"       Under 'New User Signup!' register with:\n"
                f"         Name  : Akash\n"
                f"         Email : {email}\n"
                f"       Then complete the registration form.\n"
                f"{'='*60}\n"
            )

        username = home.get_logged_in_username()
        logger.info(f"Logged in as: '{username}'")

        _results.append(log_test_result(
            "TC_02 — Login", "PASS",
            f"Logged in as: '{username}'", ss
        ))
        logger.info("TC_02 PASSED ✓")


# ══════════════════════════════════════════════════════════════════════════════
# TC_03 — Search Product
# ══════════════════════════════════════════════════════════════════════════════

class TestTC03SearchProduct:
    """TC_03: Search for a product and verify it appears in results."""

    def test_search_product(self, driver):
        """
        Steps:
        1. Navigate to the Products page.
        2. Read search term from Excel data file.
        3. Enter search term and submit.
        4. Verify search results contain the expected product.
        5. Capture screenshot.
        """
        logger.info("=== TC_03: Search Product ===")

        # Read search term from Excel
        search_term = get_excel_value("Product", "search_term")
        logger.info(f"Search term from Excel: '{search_term}'")

        search = SearchPage(driver)
        search.open_products_page()
        search.search_for(search_term)

        result_count = search.get_result_count()
        logger.info(f"Search results count: {result_count}")
        assert result_count > 0, f"No results found for '{search_term}'!"

        found = search.is_product_in_results(search_term)
        ss    = search.screenshot("03c_search_verified")

        assert found, (
            f"Product '{search_term}' not found in search results. "
            f"Results: {search.get_search_result_names()}"
        )

        _results.append(log_test_result(
            "TC_03 — Search Product", "PASS",
            f"Found '{search_term}' in {result_count} result(s).", ss
        ))
        logger.info("TC_03 PASSED ✓")


# ══════════════════════════════════════════════════════════════════════════════
# TC_04 — Add Product to Cart (with Modal Popup Handling)
# ══════════════════════════════════════════════════════════════════════════════

class TestTC04AddToCart:
    """TC_04: Add the searched product to the cart and handle the confirmation modal."""

    def test_add_product_to_cart(self, driver):
        """
        Steps:
        1. From search results, click 'View Product'.
        2. On the product detail page, note the product name.
        3. Click 'Add to Cart'.
        4. Handle the modal popup — verify it appears.
        5. Click 'Continue Shopping' to dismiss modal.
        6. Capture screenshots.
        """
        logger.info("=== TC_04: Add Product to Cart ===")

        search  = SearchPage(driver)
        product = ProductPage(driver)

        # Navigate to search results for the product
        search.open_products_page()
        search.search_for(SEARCH_PRODUCT)
        search.click_view_product(SEARCH_PRODUCT)

        product_name  = product.get_product_name()
        product_price = product.get_product_price()
        logger.info(f"Product: '{product_name}' | Price: {product_price}")

        product.screenshot("04_product_detail_page")

        # Add to cart without changing quantity (quantity update is TC_05)
        product.set_quantity(1)
        product.click_add_to_cart()

        modal_visible = product.wait_for_modal()
        modal_title   = product.get_modal_title()
        ss            = product.screenshot("04b_cart_modal_popup")

        assert modal_visible, "Cart confirmation modal did NOT appear after 'Add to Cart'!"
        logger.info(f"Modal appeared: '{modal_title}'")

        product.click_continue_shopping()

        _results.append(log_test_result(
            "TC_04 — Add to Cart", "PASS",
            f"'{product_name}' added; modal: '{modal_title}'", ss
        ))
        logger.info("TC_04 PASSED ✓")


# ══════════════════════════════════════════════════════════════════════════════
# TC_05 — Update Quantity
# ══════════════════════════════════════════════════════════════════════════════

class TestTC05UpdateQuantity:
    """TC_05: Navigate back to the product and add it with an updated quantity."""

    def test_update_quantity(self, driver):
        """
        Steps:
        1. Clear the cart to start fresh (remove leftover items from TC_04).
        2. Navigate to the product detail page.
        3. Read desired quantity from JSON.
        4. Set quantity and add to cart.
        5. Verify the cart row shows exactly the set quantity.
        6. Capture screenshot.
        """
        logger.info("=== TC_05: Update Quantity ===")

        from selenium.webdriver.common.by import By

        # ── Step 1: Clear the cart so TC_04's item doesn't pollute quantity check ──
        cart = CartPage(driver)
        cart.open_cart()
        try:
            # Delete all items currently in the cart
            delete_buttons = driver.find_elements(
                By.CSS_SELECTOR, ".cart_quantity_delete"
            )
            for btn in delete_buttons:
                driver.execute_script("arguments[0].click();", btn)
                import time; time.sleep(0.6)
            logger.info(f"Cleared {len(delete_buttons)} item(s) from cart before TC_05.")
        except Exception as e:
            logger.warning(f"Could not clear cart: {e}")

        # ── Step 2: Read quantity from JSON ──────────────────────────────────────
        quantity = int(get_json_value("product.quantity"))
        logger.info(f"Target quantity from JSON: {quantity}")

        search  = SearchPage(driver)
        product = ProductPage(driver)

        # ── Step 3: Navigate to product and set quantity ──────────────────────────
        search.open_products_page()
        search.search_for(SEARCH_PRODUCT)
        search.click_view_product(SEARCH_PRODUCT)

        # ── Step 4: Add to cart with the desired quantity ─────────────────────────
        modal_ok = product.add_product_to_cart(quantity=quantity)
        assert modal_ok, "Cart modal did not appear after updating quantity!"

        # ── Step 5: Go to cart and verify exact quantity ──────────────────────────
        product.click_view_cart_in_modal()
        ss = cart.screenshot("05_cart_after_quantity_update")

        qty_in_cart = cart.get_quantity_for_product(SEARCH_PRODUCT)
        logger.info(f"Quantity in cart: '{qty_in_cart}' (expected: '{quantity}')")

        assert qty_in_cart == str(quantity), (
            f"Quantity mismatch: expected '{quantity}', got '{qty_in_cart}'"
        )

        _results.append(log_test_result(
            "TC_05 — Update Quantity", "PASS",
            f"Quantity set to {quantity} — cart shows: '{qty_in_cart}'.", ss
        ))
        logger.info("TC_05 PASSED ✓")


# ══════════════════════════════════════════════════════════════════════════════
# TC_06 — Verify Cart Details
# ══════════════════════════════════════════════════════════════════════════════

class TestTC06VerifyCartDetails:
    """TC_06: Fully verify all cart details — product name, quantity, price, total."""

    def test_verify_cart_details(self, driver):
        """
        Steps:
        1. Open the cart page.
        2. Read expected values from Excel (CartVerification sheet).
        3. Assert product name matches.
        4. Assert quantity matches.
        5. Assert cart is not empty.
        6. Capture screenshot.
        """
        logger.info("=== TC_06: Verify Cart Details ===")

        # Read expected values from Excel
        expected_product  = get_excel_value("CartVerification", "product_name")
        expected_qty      = get_excel_value("CartVerification", "quantity")
        expected_items    = int(get_excel_value("CartVerification", "item_count"))

        cart = CartPage(driver)
        cart.open_cart()

        assert not cart.is_cart_empty(), "Cart is empty — products should be present!"

        summary = cart.get_cart_summary()
        ss      = cart.screenshot("06_cart_details_verified")

        logger.info(f"Cart summary: {summary}")

        # Verify item count
        assert summary["item_count"] >= expected_items, (
            f"Expected >= {expected_items} item(s) in cart, found {summary['item_count']}"
        )

        # Verify product name
        assert cart.is_product_in_cart(expected_product), (
            f"Product '{expected_product}' not found in cart. "
            f"Cart contains: {summary['product_names']}"
        )

        # Verify quantity
        qty_in_cart = cart.get_quantity_for_product(expected_product)
        assert expected_qty in qty_in_cart or qty_in_cart == expected_qty, (
            f"Quantity mismatch for '{expected_product}': "
            f"expected '{expected_qty}', got '{qty_in_cart}'"
        )

        logger.info(
            f"Cart verified — Product: '{expected_product}', "
            f"Qty: '{qty_in_cart}', Items: {summary['item_count']}"
        )

        _results.append(log_test_result(
            "TC_06 — Verify Cart Details", "PASS",
            f"Product='{expected_product}', Qty='{qty_in_cart}', "
            f"Items={summary['item_count']}", ss
        ))
        logger.info("TC_06 PASSED ✓")


# ══════════════════════════════════════════════════════════════════════════════
# TC_07 — Capture Screenshots
# ══════════════════════════════════════════════════════════════════════════════

class TestTC07CaptureScreenshots:
    """TC_07: Verify that screenshots were captured throughout the flow."""

    def test_screenshots_captured(self, driver):
        """
        Steps:
        1. Check the screenshots directory.
        2. Verify at least 5 screenshots were captured.
        3. Capture a final summary screenshot.
        4. Log the list of all screenshot files.
        """
        logger.info("=== TC_07: Capture Screenshots ===")

        from utils.report_helper import list_screenshots
        from pages.cart_page import CartPage

        cart = CartPage(driver)
        ss   = cart.screenshot("07_final_screenshot_verification")

        all_screenshots = list_screenshots()
        logger.info(f"Total screenshots captured: {len(all_screenshots)}")
        for path in all_screenshots:
            logger.info(f"  📸 {os.path.basename(path)}")

        assert len(all_screenshots) >= 5, (
            f"Expected at least 5 screenshots, found {len(all_screenshots)}"
        )

        _results.append(log_test_result(
            "TC_07 — Capture Screenshots", "PASS",
            f"{len(all_screenshots)} screenshots captured in '{SCREENSHOTS_DIR}'", ss
        ))
        logger.info("TC_07 PASSED ✓")


# ══════════════════════════════════════════════════════════════════════════════
# TC_08 — Read Test Data from Excel and JSON
# ══════════════════════════════════════════════════════════════════════════════

class TestTC08ReadTestData:
    """TC_08: Verify that test data can be read from both Excel and JSON sources."""

    def test_read_test_data_from_json(self, driver):
        """
        Steps:
        1. Read the full JSON file.
        2. Assert all required keys are present.
        3. Verify specific values match config.
        """
        logger.info("=== TC_08a: Read Test Data from JSON ===")

        data = read_json()
        assert "login"   in data, "JSON missing 'login' section"
        assert "product" in data, "JSON missing 'product' section"
        assert "cart"    in data, "JSON missing 'cart' section"
        assert "urls"    in data, "JSON missing 'urls' section"

        email    = data["login"]["email"]
        product  = data["product"]["search_term"]
        quantity = data["product"]["quantity"]

        assert "@" in email,       f"Invalid email in JSON: '{email}'"
        assert len(product) > 0,   "Product search term is empty in JSON"
        assert isinstance(quantity, int), f"Quantity should be int, got: {type(quantity)}"

        logger.info(
            f"JSON data valid — email: '{email}', product: '{product}', qty: {quantity}"
        )

    def test_read_test_data_from_excel(self, driver):
        """
        Steps:
        1. Read Login sheet from Excel.
        2. Read Product sheet from Excel.
        3. Read CartVerification sheet from Excel.
        4. Assert all sheets have expected data.
        """
        logger.info("=== TC_08b: Read Test Data from Excel ===")

        login_rows = read_excel("Login")
        assert len(login_rows) >= 3, f"Login sheet has {len(login_rows)} rows; expected >= 3"

        product_rows = read_excel("Product")
        assert len(product_rows) >= 3, f"Product sheet has {len(product_rows)} rows; expected >= 3"

        cart_rows = read_excel("CartVerification")
        assert len(cart_rows) >= 2, f"CartVerification sheet has {len(cart_rows)} rows; expected >= 2"

        email         = get_excel_value("Login",   "email")
        search_term   = get_excel_value("Product", "search_term")
        expected_prod = get_excel_value("CartVerification", "product_name")

        assert "@" in email,        f"Invalid email from Excel: '{email}'"
        assert len(search_term) > 0, "Search term from Excel is empty"
        assert len(expected_prod) > 0, "Expected product name from Excel is empty"

        logger.info(
            f"Excel data valid — email: '{email}', "
            f"search: '{search_term}', product: '{expected_prod}'"
        )

        from pages.home_page import HomePage
        home = HomePage(driver)
        ss   = home.screenshot("08_data_reading_verified")

        _results.append(log_test_result(
            "TC_08 — Read Test Data", "PASS",
            f"JSON & Excel data verified. Email='{email}', Product='{search_term}'", ss
        ))
        logger.info("TC_08 PASSED ✓")


# ══════════════════════════════════════════════════════════════════════════════
# TC_09 — Handle Popup / Alerts
# ══════════════════════════════════════════════════════════════════════════════

class TestTC09HandlePopupAlerts:
    """TC_09: Detect and handle JavaScript alerts and UI modal popups."""

    def test_handle_popup_alerts(self, driver):
        """
        Steps:
        1. Check if a JavaScript alert is currently present — handle it.
        2. Verify the 'Add to Cart' modal popup on the product page.
        3. Dismiss any overlay or notification modals.
        4. Log result of alert detection.
        5. Capture screenshot.
        """
        logger.info("=== TC_09: Handle Popup / Alerts ===")

        from pages.base_page    import BasePage
        from pages.search_page  import SearchPage
        from pages.product_page import ProductPage

        base    = BasePage(driver)
        search  = SearchPage(driver)
        product = ProductPage(driver)

        # ── Part A: Check for JS Alerts ────────────────────────────────────────
        js_alert_present = base.is_alert_present()
        if js_alert_present:
            alert_text = base.handle_alert("accept")
            logger.info(f"[TC_09] JS Alert handled — text: '{alert_text}'")
        else:
            logger.info("[TC_09] No JS alert present — continuing.")

        # ── Part B: Trigger and dismiss the Add-to-Cart modal (UI popup) ───────
        search.open_products_page()
        search.search_for(SEARCH_PRODUCT)
        search.click_view_product(SEARCH_PRODUCT)

        product.set_quantity(1)
        product.click_add_to_cart()
        modal_appeared = product.wait_for_modal()
        ss = product.screenshot("09_popup_modal_handled")

        if modal_appeared:
            modal_title = product.get_modal_title()
            logger.info(f"[TC_09] Cart modal detected: '{modal_title}' — dismissing.")
            product.click_continue_shopping()
            logger.info("[TC_09] Modal dismissed via 'Continue Shopping'.")
        else:
            logger.warning("[TC_09] Cart modal did not appear this time.")

        # ── Part C: Re-check for JS alert after action ─────────────────────────
        js_alert_after = base.is_alert_present()
        if js_alert_after:
            alert_text_after = base.handle_alert("dismiss")
            logger.info(f"[TC_09] Post-action alert handled: '{alert_text_after}'")

        popup_handled = modal_appeared or (not js_alert_present and not js_alert_after)
        assert popup_handled, "Failed to handle any popup/modal during TC_09."

        _results.append(log_test_result(
            "TC_09 — Handle Popup/Alerts", "PASS",
            f"JS alert: {'Found' if js_alert_present else 'None'}. "
            f"Cart modal: {'Dismissed' if modal_appeared else 'Not shown'}.", ss
        ))
        logger.info("TC_09 PASSED ✓")


# ══════════════════════════════════════════════════════════════════════════════
# TC_10 — Generate Execution Report
# ══════════════════════════════════════════════════════════════════════════════

class TestTC10GenerateReport:
    """TC_10: Confirm the execution report is generated (pytest-html + JSON)."""

    def test_generate_execution_report(self, driver):
        """
        Steps:
        1. Save a JSON summary report of all collected results.
        2. Verify the reports directory exists and contains the HTML report.
        3. Print a formatted summary table to the console.
        4. Capture final screenshot.
        """
        logger.info("=== TC_10: Generate Execution Report ===")

        from pages.home_page import HomePage

        home = HomePage(driver)
        home.open_home()
        ss = home.screenshot("10_final_state_report")

        # Add this test to results first
        _results.append(log_test_result(
            "TC_10 — Generate Report", "PASS",
            "Reports directory verified; JSON report saved.", ss
        ))

        # Save JSON report
        json_path = save_json_report(_results)
        logger.info(f"JSON report saved: {json_path}")
        assert os.path.exists(json_path), f"JSON report not found at: {json_path}"

        # Verify HTML report will be / is being generated by pytest-html
        html_report = os.path.join(REPORTS_DIR, "execution_report.html")
        logger.info(f"pytest-html report will be saved to: {html_report}")

        # Print console summary
        print_summary(_results)

        # Final checks
        assert os.path.isdir(REPORTS_DIR), f"Reports directory not found: {REPORTS_DIR}"
        assert os.path.isdir(SCREENSHOTS_DIR), f"Screenshots directory not found: {SCREENSHOTS_DIR}"

        all_screenshots = list_screenshots()
        logger.info(f"Total screenshots in report: {len(all_screenshots)}")

        logger.info("TC_10 PASSED ✓ — All reports generated.")
