from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
driver=webdriver.Firefox()
driver.get("https://rahulshettyacademy.com/AutomationPractice/#top")
driver.maximize_window()
element=driver.find_element(By.ID,"name")
action=ActionChains(driver)
target=driver.find_element(By.ID,"displayed-text")
action.move_to_element(element)
action.click()
action.send_keys("Hello")
action.key_down(Keys.CONTROL)
action.send_keys("a")
action.key_up(Keys.CONTROL)
action.key_down(Keys.CONTROL)
action.send_keys("c")
action.key_up(Keys.CONTROL)
action.move_to_element(target)
action.click()
action.key_down(Keys.CONTROL)
action.send_keys("v")
action.key_up(Keys.CONTROL)
action.perform()

