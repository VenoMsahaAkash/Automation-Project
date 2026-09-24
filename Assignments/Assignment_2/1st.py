from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
driver = webdriver.Firefox(options=options)
driver.get("https://www.google.com")
driver.switch_to.new_window("tab")
driver.get("https://www.youtube.com")