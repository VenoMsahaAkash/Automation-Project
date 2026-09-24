from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://testautomationpractice.blogspot.com/")
wait = WebDriverWait(driver, 10)
driver.find_element(By.XPATH,"//button[contains(text(),'Simple Alert')]").click()
wait.until(EC.alert_is_present())
alert = Alert(driver)
message = alert.text
print("Alert Message:", message)
alert.accept()
driver.quit()