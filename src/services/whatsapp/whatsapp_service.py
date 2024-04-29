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


class WhatsappService:
    @staticmethod
    def find_element_with_condition(driver: WebDriver, condition, timeout: int = 10):
        try:
            return WebDriverWait(driver, timeout).until(condition)
        except TimeoutException as e:
            print(f"Failed to find element with condition '{condition}': {str(e)}")
            return None

    @staticmethod
    def find_chrome_dir():
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
        # return  chrome_dir
        return '/Users/ravivs/Library/Application Support/Google/Chrome/Default'

    @staticmethod
    def get_chrome_profiles():
        chrome_dir = WhatsappService.find_chrome_dir()
        if chrome_dir is None or not os.path.exists(chrome_dir):
            return []
        profiles = []
        for subdir in os.listdir(chrome_dir):
            profile_path = os.path.join(chrome_dir, subdir)
            if os.path.isdir(profile_path):
                profiles.append(profile_path)
        return profiles

    @staticmethod
    def send_message(contact_name: str, message: str) -> None:
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={WhatsappService.find_chrome_dir()}")
        # chrome_options.add_argument('--profile-directory=Profile 1')

        # Initialize the Chrome WebDriver using ChromeDriverManager.
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver.maximize_window()
        driver.get("https://web.whatsapp.com/")

        # Search for group name.
        element = WhatsappService.find_element_with_condition(driver, ec.element_to_be_clickable(search_field))
        element.click()
        element.send_keys(contact_name)

        # Select group name.
        element = WhatsappService.find_element_with_condition(driver, ec.element_to_be_clickable(search_field))
        element.send_keys(Keys.RETURN)

        # Type message.
        for line in message.split('\n'):
            ActionChains(driver).send_keys(line).perform()
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(
                Keys.ENTER).perform()
        ActionChains(driver).send_keys(Keys.RETURN).perform()

        # WhatsappService.find_element_with_condition(driver, ec.visibility_of_all_elements_located(message_textbox))[1]
        # .send_keys(message)

        # Send message.
        # WhatsappService.find_element_with_condition(driver, ec.element_to_be_clickable(send_button)).click()

        # Quit the WebDriver.
        time.sleep(10)
        driver.quit()
