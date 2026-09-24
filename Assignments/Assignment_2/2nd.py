from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
driver = webdriver.Firefox()
driver.get("https://www.youtube.com")
parent = driver.current_window_handle
driver.switch_to.new_window("tab")
driver.get("https://www.youtube.com")
time.sleep(3)
search = driver.find_element(By.NAME, "search_query")
search.send_keys("Numb", Keys.ENTER)
time.sleep(5)
video = driver.find_element(By.XPATH, "(//a[@id='video-title'])[1]")
ActionChains(driver).context_click(video).perform()
time.sleep(1)
ActionChains(driver).send_keys(Keys.ESCAPE).perform()
video.click()
time.sleep(5)
driver.find_element(
    By.XPATH, "//button[@aria-label='Play']"
).click()
time.sleep(10)
driver.close()
driver.switch_to.window(parent)
driver.quit()