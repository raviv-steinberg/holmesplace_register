"""
Author: raviv steinberg
Date: 03/05/2024
"""
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriverFactory:
    @staticmethod
    def initiate():
        return webdriver.Chrome(options=WebDriverFactory.__get_chrome_options())

    @staticmethod
    def __get_chrome_options():
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={WebDriverFactory.__find_chrome_dir()}")
        # chrome_options.add_argument("--headless")
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google'
        return chrome_options

    @staticmethod
    def __find_chrome_dir():
        system = platform.system()
        if system == "Darwin":  # Mac
            home_dir = os.path.expanduser("~")
            chrome_dir = os.path.join(home_dir, "Library/Application Support/Google/Chrome")
        elif system == "Windows":  # Windows
            app_data_dir = os.getenv("LOCALAPPDATA")
            chrome_dir = os.path.join(app_data_dir, "Google/Chrome/User Data")
        elif system == "Linux":  # Linux
            home_dir = os.path.expanduser("~")
            chrome_dir = os.path.join(home_dir, ".config/google-chrome")
        else:
            chrome_dir = None
        directory = os.path.join(chrome_dir, 'Default')
        return directory

