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
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from src.services.selenium.web_actions import WebActions
from src.services.selenium.webdriver_factory import WebDriverFactory

search_field = (By.XPATH, "//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")
message_textbox = (By.XPATH, "//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")
send_button = (By.XPATH, "//span[@data-icon='send']")
url = 'https://web.whatsapp.com/'


class WhatsappService:
    def __init__(self, ):
        # self.logger = logger
        self.driver = WebDriverFactory.initiate()
        self.web_actions = WebActions(self.driver)

    def send_message(self, contact_name: str, message: str) -> None:
        # Search for contact name.
        element = self.web_actions.find_element_with_condition(ec.element_to_be_clickable(search_field))
        time.sleep(0.3)
        element.click()
        element.send_keys(contact_name)
        time.sleep(0.3)
        # self.logger.debug(msg=f'Search for contact {contact_name}')

        # Select contact name.
        element = self.web_actions.find_element_with_condition(ec.element_to_be_clickable(search_field))
        time.sleep(0.3)
        element.send_keys(Keys.RETURN)
        # self.logger.debug(msg=f'Contact {contact_name} selected')

        # Type message.
        for line in message.split('\n'):
            ActionChains(self.driver).send_keys(line).perform()
            time.sleep(0.3)
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(
                Keys.ENTER).perform()
            time.sleep(0.3)
        # self.logger.debug(msg='The message has been written')

        ActionChains(self.driver).send_keys(Keys.RETURN).perform()
        time.sleep(0.3)
        # self.logger.info(msg='Message sent')

        # WhatsappService.find_element_with_condition(driver, ec.visibility_of_all_elements_located(message_textbox))[1]
        # .send_keys(message)

        # Send message.
        # WhatsappService.find_element_with_condition(driver, ec.element_to_be_clickable(send_button)).click()

        # Quit the WebDriver.
        # self.logger.debug(msg='Sleep 30 seconds')
        time.sleep(2)
        # self.logger.debug(msg='Quit WebDriver')

    def open_whatsapp_session(self) -> None:
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        # self.logger.debug(msg='Window maximized')
        self.driver.maximize_window()
        # self.logger.debug(msg=f'Navigate to url {url}')
        self.driver.get(url)

    def close_driver(self) -> None:
        self.driver.quit()
