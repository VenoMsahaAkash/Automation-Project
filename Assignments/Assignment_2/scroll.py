from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Open Chrome
driver = webdriver.Chrome()

# Open website
driver.get("https://text-compare.com")

# Maximize browser
driver.maximize_window()

# Create ActionChains object
act = ActionChains(driver)

# Scroll to the bottom of the webpage
act.send_keys(Keys.END).perform()

# Locate About link
about = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.LINK_TEXT, "About")
    )
)

# Scroll About into the visible area
driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    about
)

# Click About using ActionChains
act.click(about).perform()