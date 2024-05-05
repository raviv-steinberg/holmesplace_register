"""
Author: raviv steinberg
Date: 03/05/2024
"""
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class WebActions:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def find_element_with_condition(self, condition, timeout: int = 60):
        try:
            return WebDriverWait(self.driver, timeout).until(condition)
        except TimeoutException as e:
            print(f"Failed to find element with condition '{condition}': {str(e)}")
            return None
