from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()

driver.get("https://testautomationpractice.blogspot.com/")

wait = WebDriverWait(driver, 10)

# Find "Point Me"
point_me = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//button[normalize-space()='Point Me']")
    )
)

# Scroll Point Me into the viewport
driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    point_me
)

time.sleep(1)

# Hover over Point Me
ActionChains(driver).move_to_element(point_me).perform()

# Wait for Mobiles
mobiles = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//a[normalize-space()='Mobiles']")
    )
)

# Click Mobiles
mobiles.click()

print("Mobiles selected successfully")

time.sleep(2)

driver.quit()