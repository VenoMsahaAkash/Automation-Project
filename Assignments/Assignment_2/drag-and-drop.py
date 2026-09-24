from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.maximize_window()

driver.get("https://testautomationpractice.blogspot.com/")

wait = WebDriverWait(driver, 10)

source = wait.until(
    EC.visibility_of_element_located(
        (By.ID, "draggable")
    )
)

target = wait.until(
    EC.visibility_of_element_located(
        (By.ID, "droppable")
    )
)

actions = ActionChains(driver)

actions.drag_and_drop(
    source,
    target
).perform()

driver.quit()