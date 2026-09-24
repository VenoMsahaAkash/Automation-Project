import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def before_all(context):

    context.target_url = os.getenv(
        "TARGET_URL",
        "http://127.0.0.1:5000"
    )


def before_scenario(context, scenario):

    options = Options()

    # Firefox window size
    options.add_argument("-width=1400")
    options.add_argument("-height=900")

    # Run Firefox without GUI if required
    if os.getenv("HEADLESS") == "1":
        options.add_argument("-headless")

    # Start Firefox
    context.driver = webdriver.Firefox(
        options=options
    )

    # Implicit wait
    context.driver.implicitly_wait(3)


def after_scenario(context, scenario):

    if getattr(context, "driver", None):
        context.driver.quit()