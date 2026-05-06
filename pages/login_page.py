from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # 🔹 Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    DASHBOARD_TEXT = (By.XPATH, "//h6[text()='Dashboard']")

    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Logout']")

    # 🔹 Actions
    def open(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))

    def enter_username(self, username):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).send_keys(username)

    def enter_password(self, password):
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT)).send_keys(password)

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # 🔥 CLEAN LOGOUT FLOW (WITH 20 SEC VISUAL TIMER)
    def logout(self):
        # Step 1: open user dropdown
        self.wait.until(
            EC.element_to_be_clickable(self.USER_DROPDOWN)
        ).click()

        time.sleep(1)

        # Step 2: click logout
        self.wait.until(
            EC.element_to_be_clickable(self.LOGOUT_LINK)
        ).click()

        # 🔥 20 SECOND VISUAL PAUSE (FOR YOUR EYES ONLY)
        time.sleep(20)

        # Step 3: confirm login page is back
        self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )

    # 🔹 Validation helper
    def is_logged_in(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.DASHBOARD_TEXT)
            ).is_displayed()
        except:
            return False

    def is_logged_out(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.USERNAME_INPUT)
            ).is_displayed()
        except:
            return False








# PYTHONPATH=. pytest -v -s
