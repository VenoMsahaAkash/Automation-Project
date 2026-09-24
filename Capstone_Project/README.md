# Capstone Assignment 1 — E-Commerce Web Automation with Selenium WebDriver

> **Course:** Software Test Automation | **Deadline:** 28 September 2026  
> **Application Under Test:** [automationexercise.com](https://automationexercise.com/)  
> **Language:** Python 3.x | **Framework:** Selenium WebDriver + pytest

---

## 📌 Business Scenario

A customer wants to purchase a product from an E-Commerce website.
This automation project simulates the complete end-to-end purchase flow.

---

## ✅ Test Scenarios Covered

| # | Test Case | Description |
|---|-----------|-------------|
| TC_01 | Launch Browser | Open Chrome and verify home page loads |
| TC_02 | Login to Application | Authenticate using credentials from JSON/Excel |
| TC_03 | Search Product | Search for "Blue Top" and verify results |
| TC_04 | Add Product to Cart | Add product and handle the confirmation modal popup |
| TC_05 | Update Quantity | Set quantity to 2 and add to cart |
| TC_06 | Verify Cart Details | Assert product name, quantity, and item count in cart |
| TC_07 | Capture Screenshots | Verify screenshots are auto-captured at each step |
| TC_08 | Read Test Data | Validate reading from both Excel (.xlsx) and JSON |
| TC_09 | Handle Popup/Alerts | Detect JS alerts and dismiss UI modal popups |
| TC_10 | Generate Report | Produce pytest-html + JSON execution report |

---

## 🗂️ Project Structure

```
Capstone_Project/
├── config/
│   └── config.py              # URLs, credentials, browser settings, paths
├── data/
│   ├── test_data.json         # JSON test data (credentials, product, cart)
│   └── test_data.xlsx         # Excel test data (3 sheets: Login, Product, Cart)
├── pages/                     # Page Object Model (POM)
│   ├── base_page.py           # Reusable Selenium helpers
│   ├── home_page.py           # Home page & navigation
│   ├── login_page.py          # Login form & verification
│   ├── search_page.py         # Product search & results
│   ├── product_page.py        # Product detail & Add-to-Cart
│   └── cart_page.py           # Cart verification
├── tests/
│   └── test_ecommerce_flow.py # Main test suite — all 10 scenarios
├── utils/
│   ├── data_reader.py         # Excel & JSON reader utilities
│   ├── screenshot_helper.py   # Timestamped screenshot capture
│   └── report_helper.py       # JSON report & console summary
├── screenshots/               # Auto-created — PNG screenshots per step
├── reports/                   # Auto-created — HTML & JSON reports
├── conftest.py                # pytest fixtures & screenshot-on-failure hook
├── pytest.ini                 # pytest configuration
├── create_excel_data.py       # Run once to generate test_data.xlsx
└── requirements.txt           # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. Prerequisites

- Python 3.9 or higher
- Google Chrome (latest version)
- Git

### 2. Clone the Repository

```bash
git clone <your-repo-url>
cd Capstone_Project
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Register a Test Account

> ⚠️ **Important:** You must register a free account on [automationexercise.com](https://automationexercise.com/login) first.

1. Go to https://automationexercise.com/login
2. Under **"New User Signup!"**, enter a name and email
3. Complete the registration form
4. Update **`config/config.py`** with your credentials:
   ```python
   LOGIN_EMAIL    = "your_email@example.com"
   LOGIN_PASSWORD = "YourPassword123"
   ```
5. Also update **`data/test_data.json`**:
   ```json
   "login": {
     "email": "your_email@example.com",
     "password": "YourPassword123"
   }
   ```

### 6. Generate Excel Test Data File

```bash
python create_excel_data.py
```

This creates `data/test_data.xlsx` with 3 formatted worksheets.

---

## ▶️ Running the Tests

### Run all 10 test scenarios (generates HTML report):

```bash
pytest tests/ -v
```

### Run with live console output:

```bash
pytest tests/ -v -s
```

### Run a specific test class:

```bash
pytest tests/test_ecommerce_flow.py::TestTC01LaunchBrowser -v
pytest tests/test_ecommerce_flow.py::TestTC02Login -v
```

### Run in headless mode (no browser window):

```bash
# Edit config/config.py: set HEADLESS = True
pytest tests/ -v
```

---

## 📊 Execution Report

After running, open the generated HTML report in your browser:

```
reports/execution_report.html
```

A JSON report is also saved at:

```
reports/test_results.json
```

---

## 📸 Screenshots

All screenshots are timestamped and saved automatically to:

```
screenshots/
  20260908_104523_01_home_page_loaded.png
  20260908_104530_02a_login_page.png
  20260908_104535_02b_after_login.png
  ... (one per step)
  20260908_104600_FAILED_<testname>.png   ← auto-captured on failures
```

---

## 🏗️ Design Pattern

This project uses the **Page Object Model (POM)** design pattern:

- Each web page has its own Python class in `pages/`
- All Selenium locators are kept inside their respective page class
- Test methods in `tests/` only call page methods — no raw Selenium in tests
- `BasePage` provides shared utilities (wait, click, type, screenshot, alerts)

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| selenium | 4.18.1 | Browser automation |
| webdriver-manager | 4.0.1 | Auto-install ChromeDriver |
| pytest | 8.1.1 | Test runner |
| pytest-html | 4.1.1 | HTML execution report |
| openpyxl | 3.1.2 | Read/write Excel (.xlsx) |
| Pillow | 10.2.0 | Image utilities |

---

## 📁 GitHub Repository Structure

```
GitHub Repo/
├── Folder 1 - Lab Work and Video Demonstrations/
│   └── (module-wise lab work and videos)
├── Folder 2 - Capstone Project/          ← This project
│   ├── (all source code as above)
│   ├── reports/
│   ├── screenshots/
│   └── README.md
└── Folder 3 - Certificates/
    └── (course completion certificates)
```

---

## 👤 Author

- **Student Name:** AKASH SAHA
- **Course:** Software Test Automation with Selenium WebDriver
- **Institution:** INSTITUATION OF ENGINEERING AND MANAGEMENT
- 
