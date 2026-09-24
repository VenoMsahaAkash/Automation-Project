from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://testautomationpractice.blogspot.com/")
wait = WebDriverWait(driver, 10)
# Step 3: Locate the keyboard input field
input_box = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//textarea[@id='textarea']")
    )
)

input_box.click()

input_box.send_keys("Selenium Automation")

actions = ActionChains(driver)

actions.key_down(Keys.CONTROL) \
       .send_keys("a") \
       .key_up(Keys.CONTROL) \
       .perform()

# Step 7: Delete selected text
input_box.send_keys(Keys.BACKSPACE)

input_box.send_keys("Python Selenium")
input_box.send_keys(Keys.ENTER)
driver.quit()