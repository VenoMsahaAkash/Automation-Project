from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()

driver.get("https://testautomationpractice.blogspot.com/")

wait = WebDriverWait(driver, 10)

# 1. Find source
source = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//p[normalize-space()='Drag me to my target']")
    )
)

# 2. Find target
target = wait.until(
    EC.visibility_of_element_located(
        (By.ID, "droppable")
    )
)

# 3. Scroll TARGET into the viewport
driver.execute_script(
    """
    arguments[0].scrollIntoView({
        block: 'center',
        inline: 'center'
    });
    """,
    target
)

time.sleep(1)

# 4. Scroll SOURCE into viewport
driver.execute_script(
    """
    arguments[0].scrollIntoView({
        block: 'center',
        inline: 'center'
    });
    """,
    source
)

time.sleep(1)

# 5. Scroll TARGET again because scrolling source may move target
driver.execute_script(
    """
    arguments[0].scrollIntoView({
        block: 'center',
        inline: 'center'
    });
    """,
    target
)

time.sleep(1)

# 6. Perform drag and drop
actions = ActionChains(driver)

actions.click_and_hold(source) \
       .move_to_element(target) \
       .release() \
       .perform()

time.sleep(2)

print("Drag and drop completed")

driver.quit()