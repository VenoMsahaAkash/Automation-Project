# 🛒 Capstone Assignment 1 — E-Commerce Web Automation

**Course:** Software Test Automation
**Application Under Test:** [Automation Exercise](https://automationexercise.com/)
**Language:** Python 3.x
**Framework:** Selenium WebDriver + pytest
**Design Pattern:** Page Object Model (POM)

---

## 📌 Project Overview

This project implements an end-to-end **E-Commerce Web Automation Framework** using **Python, Selenium WebDriver, and pytest**.

The automation simulates a customer's purchase journey on the Automation Exercise website, covering login, product search, cart operations, data-driven testing, popup handling, screenshot capture, and test reporting.

The project follows the **Page Object Model (POM)** design pattern to keep the automation framework modular, reusable, and maintainable.

---

## 🎯 Business Scenario

A customer wants to purchase a product from an E-Commerce website.

This automation project simulates the complete purchase flow:

```text
Launch Website
      ↓
Login
      ↓
Search Product
      ↓
Select Product
      ↓
Add to Cart
      ↓
Update Quantity
      ↓
Verify Cart
      ↓
Generate Test Report
```

---

## ✅ Test Scenarios Covered

| Test Case | Description          | Validation                                           |
| --------- | -------------------- | ---------------------------------------------------- |
| **TC_01** | Launch Browser       | Open Chrome and verify the home page                 |
| **TC_02** | Login to Application | Authenticate using test credentials                  |
| **TC_03** | Search Product       | Search for **Blue Top** and verify results           |
| **TC_04** | Add Product to Cart  | Add product and handle confirmation modal            |
| **TC_05** | Update Quantity      | Set product quantity to **2**                        |
| **TC_06** | Verify Cart Details  | Verify product name, quantity, and item count        |
| **TC_07** | Capture Screenshots  | Automatically capture screenshots at important steps |
| **TC_08** | Read Test Data       | Validate reading data from JSON and Excel            |
| **TC_09** | Handle Popups/Alerts | Detect and dismiss JavaScript alerts and UI modals   |
| **TC_10** | Generate Reports     | Generate HTML and JSON execution reports             |

---

## 🛠️ Technologies & Tools

| Technology             | Purpose                             |
| ---------------------- | ----------------------------------- |
| **Python 3.x**         | Programming language                |
| **Selenium WebDriver** | Browser automation                  |
| **pytest**             | Test execution framework            |
| **Page Object Model**  | Automation framework design pattern |
| **openpyxl**           | Excel data handling                 |
| **pytest-html**        | HTML test reporting                 |
| **JSON**               | Test-data management                |
| **webdriver-manager**  | ChromeDriver management             |
| **Pillow**             | Screenshot/image utilities          |
| **Git & GitHub**       | Version control and project hosting |

---

## 🗂️ Project Structure

```text
Capstone_Project/
│
├── config/
│   └── config.py
│
├── data/
│   ├── test_data.json
│   └── test_data.xlsx
│
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── search_page.py
│   ├── product_page.py
│   └── cart_page.py
│
├── tests/
│   └── test_ecommerce_flow.py
│
├── utils/
│   ├── data_reader.py
│   ├── screenshot_helper.py
│   └── report_helper.py
│
├── screenshots/
│
├── reports/
│
├── conftest.py
├── pytest.ini
├── create_excel_data.py
├── requirements.txt
└── README.md
```

---

## 🏗️ Page Object Model (POM)

This project follows the **Page Object Model** design pattern.

Each major page of the application is represented by a dedicated Python class.

```text
pages/
├── base_page.py
├── home_page.py
├── login_page.py
├── search_page.py
├── product_page.py
└── cart_page.py
```

### Benefits of POM

* Separates test logic from page-specific implementation
* Centralizes Selenium locators
* Improves code reusability
* Makes maintenance easier
* Reduces duplicate Selenium code
* Makes test cases easier to read

The test cases call page methods instead of directly interacting with Selenium elements.

---

## 🔧 Key Features

### 1. Reusable Base Page

`base_page.py` contains common Selenium operations such as:

* Explicit waits
* Element clicking
* Text input
* Getting element text
* Screenshot capture
* JavaScript alert handling
* Common browser operations

---

### 2. Data-Driven Testing

The framework supports test data from:

```text
JSON
Excel (.xlsx)
```

The Excel file contains separate worksheets for:

```text
Login
Product
Cart
```

---

### 3. Automatic Screenshot Capture

Screenshots are automatically captured during important test steps.

Example:

```text
screenshots/
├── 20260908_104523_01_home_page_loaded.png
├── 20260908_104530_02a_login_page.png
├── 20260908_104535_02b_after_login.png
└── 20260908_104600_FAILED_test_name.png
```

Failure screenshots are also captured automatically when a test fails.

---

### 4. Popup and Alert Handling

The framework handles:

* JavaScript alerts
* Confirmation dialogs
* E-Commerce confirmation modals

This ensures that popup interactions do not interrupt the test execution.

---

### 5. Test Reporting

The framework generates both HTML and JSON reports.

```text
reports/
├── execution_report.html
└── test_results.json
```

The HTML report provides a visual summary of the test execution, while the JSON report contains structured execution results.

---

## ⚙️ Setup Instructions

### 1. Prerequisites

Install the following:

* Python 3.9 or higher
* Google Chrome
* Git

---

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd Capstone_Project
```

---

### 3. Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Create a Test Account

Create a free test account on:

[Automation Exercise](https://automationexercise.com/login)

Update the test credentials in your local configuration and test-data files.

Example:

```python
LOGIN_EMAIL = "your_email@example.com"
LOGIN_PASSWORD = "YourPassword123"
```

> ⚠️ **Important:** Never upload real passwords, API keys, or other sensitive credentials to GitHub.

---

### 6. Generate Excel Test Data

Run:

```bash
python create_excel_data.py
```

This generates:

```text
data/test_data.xlsx
```

with the following worksheets:

```text
Login
Product
Cart
```

---

## ▶️ Running the Tests

### Run All Tests

```bash
pytest tests/ -v
```

---

### Run With Live Console Output

```bash
pytest tests/ -v -s
```

---

### Run a Specific Test Class

```bash
pytest tests/test_ecommerce_flow.py::TestTC01LaunchBrowser -v
```

```bash
pytest tests/test_ecommerce_flow.py::TestTC02Login -v
```

---

### Run in Headless Mode

Set:

```python
HEADLESS = True
```

in:

```text
config/config.py
```

Then run:

```bash
pytest tests/ -v
```

---

## 📊 Test Execution Reports

After execution, the framework generates:

### HTML Report

```text
reports/execution_report.html
```

### JSON Report

```text
reports/test_results.json
```

Open the HTML report in a browser to view the execution summary.

---

## 📸 Screenshots

Screenshots are automatically stored in:

```text
screenshots/
```

Example:

```text
screenshots/
├── 20260908_104523_01_home_page_loaded.png
├── 20260908_104530_02a_login_page.png
├── 20260908_104535_02b_after_login.png
└── 20260908_104600_FAILED_test_name.png
```

---

## 📦 Dependencies

```text
selenium==4.18.1
webdriver-manager==4.0.1
pytest==8.1.1
pytest-html==4.1.1
openpyxl==3.1.2
Pillow==10.2.0
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🧪 Test Automation Architecture

```text
                    ┌───────────────────────┐
                    │      pytest Tests     │
                    │ test_ecommerce_flow.py│
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     Page Objects      │
                    │ Home / Login / Search  │
                    │ Product / Cart         │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │       BasePage        │
                    │ Wait / Click / Type    │
                    │ Alerts / Screenshots  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Selenium WebDriver  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Automation Exercise │
                    └───────────────────────┘
```

---

## 📚 Learning Outcomes

Through this project, I implemented and practiced:

* Selenium WebDriver automation
* Python-based test automation
* pytest framework
* Page Object Model
* Explicit waits
* Web element interaction
* JavaScript alert handling
* Modal popup handling
* Data-driven testing
* JSON data handling
* Excel data handling
* Automatic screenshot capture
* Failure handling
* HTML test reporting
* JSON reporting
* Reusable automation utilities
* Git and GitHub

---

## 👤 Author

**AKASH SAHA**

**B.Tech — Computer Science & Engineering (Artificial Intelligence & Machine Learning)**
**Institute of Engineering & Management, Kolkata**

**Course:** Software Test Automation with Selenium WebDriver

---

## ⭐ Project Summary

This project demonstrates an end-to-end **E-Commerce Web Automation Framework** built using **Python, Selenium WebDriver, pytest, and Page Object Model (POM)**.

It covers the complete automation workflow from **browser launch and user authentication to product search, cart validation, screenshot capture, and automated test reporting**.
