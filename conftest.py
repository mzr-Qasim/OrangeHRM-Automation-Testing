import os
import pytest
from selenium import webdriver
from utils.jira_client import JiraClient

jira = JiraClient()


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()


def pytest_runtest_makereport(item, call):

    if call.when == "call" and call.excinfo is not None:

        driver = item.funcargs.get("driver")

        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/{item.name}.png"

        current_url = "N/A"

        if driver:
            driver.save_screenshot(screenshot_path)
            current_url = driver.current_url

        # 🔥 CLEAN ERROR (NO STACKTRACE)
        error_type = call.excinfo.typename

        raw_error = str(call.excinfo.value)

        # ✔ KEEP ONLY FIRST LINE (REMOVE SELENIUM STACKTRACE)
        error_msg = raw_error.split("\n")[0]

        clean_description = f"""
Test Execution Failed

Test Name: {item.name}
URL: {current_url}

Error Type: {error_type}
Error Message: {error_msg}
"""

        jira.create_bug(
            summary=f"Test Failed: {item.name}",
            description=clean_description,
            screenshot_path=screenshot_path
        ) 