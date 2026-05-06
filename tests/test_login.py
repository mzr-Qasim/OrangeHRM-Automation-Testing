import os
from dotenv import load_dotenv

from selenium import webdriver
from pages.login_page import LoginPage

load_dotenv()


def test_login_success():
    # 🚀 Let Selenium Manager handle Firefox + driver automatically
    driver = webdriver.Firefox()
    driver.maximize_window()

    try:
        page = LoginPage(driver)
        page.open()

        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")

        assert username and password, "Missing env variables"

        page.login(username, password)

        assert page.is_logged_in()

    finally:
        driver.quit()