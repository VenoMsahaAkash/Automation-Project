from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Step 1: Launch Firefox
driver = webdriver.Firefox()
driver.maximize_window()

try:
    # Step 2: Open webpage
    driver.get("https://testautomationpractice.blogspot.com/")
    print("✓ Webpage loaded successfully")

    wait = WebDriverWait(driver, 10)

    # Step 3: Locate Point Me button
    point_me = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[normalize-space()='Point Me']")
        )
    )
    print("✓ 'Point Me' button found")

    # Step 4: Scroll to Point Me
    driver.execute_script("""
        arguments[0].scrollIntoView({
            behavior: 'instant',
            block: 'center',
            inline: 'center'
        });
    """, point_me)

    # Step 5: Wait until button is visible
    wait.until(
        EC.visibility_of(point_me)
    )

    # Step 6: Hover over Point Me
    actions = ActionChains(driver)
    actions.move_to_element(point_me).perform()

    print("✓ Mouse hovered over 'Point Me'")

    # Step 7: Locate Mobiles submenu
    mobiles = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[normalize-space()='Mobiles']")
        )
    )

    print("✓ 'Mobiles' link found")

    # Step 8: Click Mobiles
    mobiles.click()

    print("✓ 'Mobiles' clicked successfully")

except Exception as e:
    print("✗ Error occurred:", e)

finally:
    driver.quit()
    print("✓ Browser closed")