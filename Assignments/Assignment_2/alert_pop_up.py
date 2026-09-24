from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()

driver.get("https://testautomationpractice.blogspot.com/")

driver.maximize_window()
# Step 4: Click the Alert button
driver.find_element(
    By.XPATH,
    "//button[text()='Confirmation Alert']"
).click()

# Step 5: Switch to alert popup
alert = driver.switch_to.alert
print("Alert Message:", alert.text)
alert.accept()
time.sleep(10)
driver.quit()