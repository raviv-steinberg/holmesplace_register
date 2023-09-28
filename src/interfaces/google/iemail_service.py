from typing import List, Dict, Any
from src.interfaces.google.igoogle_service import IGoogleService
from abc import abstractmethod


class IEmailService(IGoogleService):
    """
    Abstract base class for email services.
    """

    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None:
        """
        Sends an email using the Gmail API.
        :param to: The recipient email address.
        :param subject: The email subject.
        :param body: The email body.
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def list_inbox_messages(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Lists the latest messages in the user's inbox.
        :param max_results: The maximum number of messages to retrieve. Defaults to 10.
        :return: A list of message details.
        """
        pass
