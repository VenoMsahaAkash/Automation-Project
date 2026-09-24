from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Open Chrome
driver = webdriver.Chrome()

# Open website
driver.get("https://text-compare.com")

# Maximize browser
driver.maximize_window()

# Locate the left text box
left_text = driver.find_element(
    By.CSS_SELECTOR,
    "textarea:nth-of-type(1)"
)

# Create ActionChains object
act = ActionChains(driver)

# Click on the left text box
act.click(left_text)

# Select all text - Ctrl + A
act.key_down(Keys.CONTROL)
act.send_keys("a")
act.key_up(Keys.CONTROL)

# Copy selected text - Ctrl + C
act.key_down(Keys.CONTROL)
act.send_keys("c")
act.key_up(Keys.CONTROL)

# Locate the right text box
right_text = driver.find_element(
    By.CSS_SELECTOR,
    "textarea:nth-of-type(2)"
)

# Click on the right text box
act.click(right_text)

# Paste text - Ctrl + V
act.key_down(Keys.CONTROL)
act.send_keys("v")
act.key_up(Keys.CONTROL)

# Perform all actions
act.perform()