import os
import platform
import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

search_field = (By.XPATH, "//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")
message_textbox = (By.XPATH, "//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")
send_button = (By.XPATH, "//span[@data-icon='send']")
url = 'https://web.whatsapp.com/'


class WhatsappService:
    def __init__(self, logger):
        self.logger = logger

    def find_element_with_condition(self, driver: WebDriver, condition, timeout: int = 60):
        try:
            return WebDriverWait(driver, timeout).until(condition)
        except TimeoutException as e:
            print(f"Failed to find element with condition '{condition}': {str(e)}")
            return None

    def find_chrome_dir(self):
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
        self.logger.debug(msg=f'Google chrome profile directory: {directory}')
        return directory

    def send_message(self, contact_name: str, message: str) -> None:
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={self.find_chrome_dir()}")
        chrome_options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

        # Initialize the Chrome WebDriver using ChromeDriverManager.
        driver = webdriver.Chrome(options=chrome_options)
        self.logger.debug(msg='Driver initiated')
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.logger.debug(msg='Window maximized')
        driver.maximize_window()
        self.logger.debug(msg=f'Navigate to url {url}')
        driver.get(url)

        # Search for contact name.
        element = self.find_element_with_condition(driver, ec.element_to_be_clickable(search_field))
        time.sleep(0.3)
        element.click()
        element.send_keys(contact_name)
        time.sleep(0.3)
        self.logger.debug(msg=f'Search for contact {contact_name}')

        # Select contact name.
        element = self.find_element_with_condition(driver, ec.element_to_be_clickable(search_field))
        time.sleep(0.3)
        element.send_keys(Keys.RETURN)
        self.logger.debug(msg=f'Contact {contact_name} selected')

        # Type message.
        for line in message.split('\n'):
            ActionChains(driver).send_keys(line).perform()
            time.sleep(0.3)
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            time.sleep(0.3)
        self.logger.debug(msg='The message has been written')

        ActionChains(driver).send_keys(Keys.RETURN).perform()
        time.sleep(0.3)
        self.logger.info(msg='Message sent')

        # WhatsappService.find_element_with_condition(driver, ec.visibility_of_all_elements_located(message_textbox))[1]
        # .send_keys(message)

        # Send message.
        # WhatsappService.find_element_with_condition(driver, ec.element_to_be_clickable(send_button)).click()

        # Quit the WebDriver.
        self.logger.debug(msg='Sleep 30 seconds')
        time.sleep(30)
        self.logger.debug(msg='Quit WebDriver')
        driver.quit()
