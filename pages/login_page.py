from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Logout']")

    # Open page
    def open(self):
        self.driver.get(
            "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        )
        self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )

    # Actions
    def enter_username(self, username):
        self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        ).send_keys(username)

    def enter_password(self, password):
        self.wait.until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        ).send_keys(password)

    def click_login(self):
        self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        ).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def logout(self):
        self.wait.until(
            EC.element_to_be_clickable(self.USER_DROPDOWN)
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(self.LOGOUT_LINK)
        ).click()