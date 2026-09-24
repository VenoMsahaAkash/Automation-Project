"""
Configuration file for the Capstone E-Commerce Automation Project.
Contains all URLs, credentials, browser settings, and timeouts.
"""

import os

# ─── Application URLs ────────────────────────────────────────────────────────
BASE_URL        = "https://automationexercise.com"
LOGIN_URL       = f"{BASE_URL}/login"
PRODUCTS_URL    = f"{BASE_URL}/products"
CART_URL        = f"{BASE_URL}/view_cart"

# ─── Test Credentials (Register at automationexercise.com first) ─────────────
# NOTE: Register a free account at https://automationexercise.com/login
#       then update the values below.
LOGIN_EMAIL    = "Put Your Email"
LOGIN_PASSWORD = "PUt your Own password "
USER_NAME      = "Akash"

# ─── Test Product ────────────────────────────────────────────────────────────
SEARCH_PRODUCT   = "Blue Top"
PRODUCT_QUANTITY = 2

# ─── Browser Settings ────────────────────────────────────────────────────────
BROWSER   = "firefox"      # Options: "chrome", "firefox", "edge"
HEADLESS  = False          # Set True to run without visible browser window

# ─── Timeouts (seconds) ──────────────────────────────────────────────────────
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 60

# ─── Output Directories ──────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
REPORTS_DIR     = os.path.join(BASE_DIR, "reports")
DATA_DIR        = os.path.join(BASE_DIR, "data")

# ─── Data Files ──────────────────────────────────────────────────────────────
JSON_DATA_FILE  = os.path.join(DATA_DIR, "test_data.json")
EXCEL_DATA_FILE = os.path.join(DATA_DIR, "test_data.xlsx")

# ─── Create output directories if not present ────────────────────────────────
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
