"""
Author: raviv steinberg
Date: 03/05/2024
"""
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class WebDriverFactory:
    """
    Provides functionality to create a WebDriver instance for Chrome with specific options
    based on the operating system of the user. The Chrome options are configured to use a
    specific user data directory.
    """

    @staticmethod
    def initiate() -> WebDriver:
        """
        Creates and returns a new instance of a Chrome WebDriver with customized options.
        :return: An instance of Chrome WebDriver.
        """
        return webdriver.Chrome(options=WebDriverFactory.__get_chrome_options())

    @staticmethod
    def __get_chrome_options() -> Options:
        """
        Configures and returns Chrome options for the WebDriver. The options include the
        path to the binary of Chrome and a user-specific data directory.
        :return: Configured Chrome options.
        """
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={WebDriverFactory.__find_chrome_dir()}")
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google'
        return chrome_options

    @staticmethod
    def __find_chrome_dir() -> str:
        """
        Determines the directory path for Chrome's user data based on the operating system.
        Supports Mac, Windows, and Linux.
        :return: A string representing the path to the user data directory for Chrome.
        :raise ValueError: If the operating system is not recognized.
        """
        system = platform.system()
        # Mac.
        if system == "Darwin":
            home_dir = os.path.expanduser("~")
            chrome_dir = os.path.join(home_dir, "Library/Application Support/Google/Chrome")
        # Windows.
        elif system == "Windows":
            app_data_dir = os.getenv("LOCALAPPDATA")
            chrome_dir = os.path.join(app_data_dir, "Google/Chrome/User Data")
        # Linux.
        elif system == "Linux":
            home_dir = os.path.expanduser("~")
            chrome_dir = os.path.join(home_dir, ".config/google-chrome")
        else:
            chrome_dir = None
        directory = os.path.join(chrome_dir, 'Default')
        return directory
