from behave import given, when, then

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import (
    Select,
    WebDriverWait
)

from selenium.webdriver.support import expected_conditions as EC


# ==========================================================
# WAIT FOR ELEMENT
# ==========================================================

def wait_for(context, locator):

    return WebDriverWait(
        context.driver,
        10
    ).until(
        EC.visibility_of_element_located(locator)
    )


# ==========================================================
# APPLICATION AVAILABLE
# ==========================================================

@given("the embedded device web application is available")
def step_app_available(context):

    context.driver.get(
        context.target_url
    )

    assert (
        "Embedded Device Login"
        in context.driver.title
    )


# ==========================================================
# OPEN LOGIN PAGE
# ==========================================================

@given("I open the device login page")
def step_open_login(context):

    context.driver.get(
        context.target_url
    )


# ==========================================================
# LOGIN
# ==========================================================

@given("I am logged in")
def step_logged_in(context):

    context.driver.get(
        context.target_url
    )

    # Username
    username = wait_for(
        context,
        (By.ID, "username")
    )

    username.send_keys("admin")

    # Password
    password = wait_for(
        context,
        (By.ID, "password")
    )

    password.send_keys("admin123")

    # Login
    login_button = wait_for(
        context,
        (By.ID, "login-button")
    )

    login_button.click()

    # Wait for dashboard
    wait_for(
        context,
        (By.ID, "dashboard-title")
    )


# ==========================================================
# ENTER USERNAME
# ==========================================================

@when('I enter username "{username}"')
def step_username(context, username):

    username_box = wait_for(
        context,
        (By.ID, "username")
    )

    username_box.clear()

    username_box.send_keys(
        username
    )


# ==========================================================
# ENTER PASSWORD
# ==========================================================

@when('I enter password "{password}"')
def step_password(context, password):

    password_box = wait_for(
        context,
        (By.ID, "password")
    )

    password_box.clear()

    password_box.send_keys(
        password
    )


# ==========================================================
# LOGIN BUTTON
# ==========================================================

@when("I click the Login button")
def step_login(context):

    login_button = wait_for(
        context,
        (By.ID, "login-button")
    )

    login_button.click()


# ==========================================================
# VERIFY DASHBOARD
# ==========================================================

@then("I should see the device dashboard")
def step_dashboard(context):

    wait_for(
        context,
        (By.ID, "dashboard-title")
    )

    assert (
        "Embedded Device Dashboard"
        in context.driver.title
    )


# ==========================================================
# VERIFY DEVICE STATUS
# ==========================================================

@then('the device status should be "{status}"')
def step_status(context, status):

    status_element = wait_for(
        context,
        (By.ID, "device-status")
    )

    actual_status = status_element.text

    expected_status = (
        f"Status: {status}"
    )

    assert actual_status == expected_status


# ==========================================================
# SELECT DEVICE MODE
# ==========================================================

@when('I select device mode "{mode}"')
def step_select_mode(context, mode):

    mode_dropdown = wait_for(
        context,
        (By.ID, "mode")
    )

    select = Select(
        mode_dropdown
    )

    select.select_by_value(
        mode
    )


# ==========================================================
# APPLY MODE
# ==========================================================

@when("I click the Apply Mode button")
def step_apply_mode(context):

    apply_button = wait_for(
        context,
        (By.ID, "apply-mode")
    )

    apply_button.click()


# ==========================================================
# VERIFY DEVICE MODE
# ==========================================================

@then('the device mode should be "{mode}"')
def step_mode(context, mode):

    mode_element = wait_for(
        context,
        (By.ID, "device-mode")
    )

    actual_mode = mode_element.text

    expected_mode = (
        f"Mode: {mode}"
    )

    assert actual_mode == expected_mode


# ==========================================================
# FEATURE BUTTON
# ==========================================================

@when("I click the feature button")
def step_feature(context):

    feature_button = wait_for(
        context,
        (By.ID, "feature-button")
    )

    feature_button.click()


# ==========================================================
# VERIFY FEATURE
# ==========================================================

@then('the feature status should be "{status}"')
def step_feature_status(context, status):

    feature_element = wait_for(
        context,
        (By.ID, "feature-status")
    )

    actual_status = feature_element.text

    expected_status = (
        f"Feature: {status}"
    )

    assert actual_status == expected_status


# ==========================================================
# INVALID LOGIN
# ==========================================================

@then('I should see the login error "{message}"')
def step_login_error(context, message):

    error_element = wait_for(
        context,
        (By.ID, "error")
    )

    actual_message = error_element.text

    assert actual_message == message


# ==========================================================
# LOGOUT
# ==========================================================

@when("I click the Logout link")
def step_logout(context):

    logout_link = wait_for(
        context,
        (By.ID, "logout")
    )

    logout_link.click()


# ==========================================================
# VERIFY LOGIN PAGE
# ==========================================================

@then("I should return to the login page")

def step_login_page(context):

    wait_for(
        context,
        (By.ID, "login-button")
    )

    assert (
        "Embedded Device Login"
        in context.driver.page_source
    )