from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


driver = None

try:
    # Selenium Manager can manage Firefox and geckodriver automatically.
    driver = webdriver.Firefox()

    # Open the public Selenium practice form.
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    # Verify that the correct page has loaded.
    expected_title = "Web form"

    if driver.title != expected_title:
        raise AssertionError(
            f"Unexpected page title: {driver.title}"
        )

    print("Page title verified:", driver.title)


    # Interaction 1: Text input
    # Locator strategy: NAME


    text_box = driver.find_element(By.NAME, "my-text")
    text_box.clear()
    text_box.send_keys("Selenium Assignment")


    # Interaction 2: Checkbox
    # Locator strategy: CSS selector


    checkbox = driver.find_element(
        By.CSS_SELECTOR,
        "input[type='checkbox']"
    )

    if not checkbox.is_selected():
        checkbox.click()

    # Interaction 3: Submit button
    # Locator strategy: TAG NAME

    submit_button = driver.find_element(By.TAG_NAME, "button")
    submit_button.click()



    wait = WebDriverWait(driver, 10)

    message = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "message")
        )
    )

    print("Confirmation message:", message.text)

    # Verify the successful result.
    if message.text != "Received!":
        raise AssertionError(
            f"Unexpected confirmation: {message.text}"
        )

    # Capture evidence after successful interaction.
    driver.save_screenshot("successful_interaction_firefox.png")

    print("Automation completed successfully.")
    print(
        "Screenshot saved as successful_interaction_firefox.png"
    )


except NoSuchElementException as error:
    # Element cannot be found.
    print("Element interaction failed.")
    print("Check the locator and page structure.")
    print("Technical details:", error)


except TimeoutException as error:
    # Required condition did not become true within the timeout.
    print("The expected page condition was not reached.")
    print("Check page loading, timing, or the locator.")
    print("Technical details:", error)


except Exception as error:
    # Unexpected failure.
    print("Unexpected automation error:")
    print(error)


finally:
    # Always close the complete WebDriver session.
    if driver is not None:
        driver.quit()

    print("Browser session closed safely.")