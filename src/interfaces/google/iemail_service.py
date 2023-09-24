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
