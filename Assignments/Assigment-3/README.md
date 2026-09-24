# Selenium Python Behave BDD QEMU Project

## Technologies

- Python
- Selenium 4
- Firefox
- Behave BDD
- Flask
- QEMU
- Visual Studio Code

## Installation

Create virtual environment:

py -3.11 -m venv .venv

Activate:

.\.venv\Scripts\Activate.ps1

Install:

pip install -r requirements.txt


## Start Mock Device

python mock_device\app.py


## Run Tests

$env:TARGET_URL="http://127.0.0.1:5000"

behave


## Headless Execution

$env:HEADLESS="1"

behave


## QEMU Execution

$env:TARGET_URL="http://127.0.0.1:8080"

behave