from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Firefox()
driver.get("https://testautomationpractice.blogspot.com/")
driver.maximize_window()
wait = WebDriverWait(driver, 10)
button = driver.find_element(By.ID, "confirmBtn")
print("Button text:", button.text)
button.click()
wait.until(EC.alert_is_present())
alert = Alert(driver)
print("Popup:", alert.text)
alert.accept()
driver.quit()