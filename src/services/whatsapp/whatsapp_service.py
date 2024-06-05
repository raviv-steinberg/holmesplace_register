import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from src.services.selenium.web_actions import WebActions
from src.services.selenium.webdriver_factory import WebDriverFactory

search_field = (By.XPATH, "//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")
message_textbox = (By.XPATH, "//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")
send_button = (By.XPATH, "//span[@data-icon='send']")
clear_search_button = (By.XPATH, "//span[@data-icon='x-alt']")
search_button = (By.XPATH, "//span[@data-icon='search']")
url = 'https://web.whatsapp.com/'


class WhatsappService:
    def __init__(self, ):
        """
        Initializes the WhatsappService with a WebDriver and a WebActions instance.
        """
        self.driver = WebDriverFactory.initiate()
        self.web_actions = WebActions(self.driver)

    def send_message(self, contact_name: str, message: str) -> None:
        """
        Sends a message to a specified contact via WhatsApp Web.
        :param contact_name: The name of the contact to whom the message will be sent.
        :param message: The message text to be sent.
        :return: None
        """
        # Search for contact name.
        element = self.web_actions.find_element_with_condition(ec.element_to_be_clickable(search_field))
        time.sleep(0.3)
        element.click()
        time.sleep(0.3)
        element.send_keys(contact_name)
        time.sleep(0.3)

        # Select contact name.
        element = self.web_actions.find_element_with_condition(ec.element_to_be_clickable(search_field))
        time.sleep(0.3)
        element.send_keys(Keys.RETURN)

        # Type message.
        for line in message.split('\n'):
            ActionChains(self.driver).send_keys(line).perform()
            time.sleep(0.3)
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(
                Keys.ENTER).perform()
            time.sleep(0.3)

        ActionChains(self.driver).send_keys(Keys.RETURN).perform()
        time.sleep(0.3)
        time.sleep(5)

    def open_whatsapp_session(self) -> None:
        """
        Opens the WhatsApp Web session by navigating to the WhatsApp Web URL and maximizing the browser window.
        :return: None
        """
        self.driver.maximize_window()
        self.driver.get(url)

    def close_driver(self) -> None:
        """
        Closes the WebDriver session.
        :return: None
        """
        self.driver.quit()
