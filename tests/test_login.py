import os
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage

load_dotenv()


def test_login_success(driver):

    page = LoginPage(driver)
    wait = WebDriverWait(driver, 10)

    page.open()

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    assert username and password, "Missing env variables"

    page.login(username, password)

    dashboard_element = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h6[text()='Dashboard']")
        )
    )

    assert dashboard_element.is_displayed()



# PYTHONPATH=. pytest -v -s
  