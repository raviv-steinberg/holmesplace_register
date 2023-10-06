import smtplib
from typing import Any, List, Dict
from src.interfaces.google.iemail_service import IEmailService
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


class SMTPService(IEmailService):
    """
    Provides the implementation for sending email notifications.
    This class derives from the INotification interface and provides the specific
    logic for sending email notifications. It handles:
        - Validating the email address.
        - Connecting to the email server.
        - Formatting the email content.
        - Sending the email.
    Exceptions related to email sending and validation are logged for troubleshooting.
    """

    def list_inbox_messages(self, max_results: int = 10) -> List[Dict[str, Any]]:
        pass

    def __init__(self):
        """
        Initializes an instance of the GoogleGmail class.
        """
        self.service = self.authenticate()

    def authenticate(self) -> Any:
        service = smtplib.SMTP_SSL(self.SMTP_SERVER_ADDRESS, self.SMTP_SERVER_PORT)
        service.ehlo()
        service.login(self.SENDER_ADDRESS, self.SENDER_PASSWORD)
        return service

    def get_scopes(self) -> list:
        pass

    SMTP_SERVER_ADDRESS = 'smtp.gmail.com'
    SMTP_SERVER_PORT = 465
    SENDER_ADDRESS = 'holmesregister@gmail.com'
    SENDER_PASSWORD = 'rabiczmlqrzsdbbz'
    SENDER_NAME = 'Holmes Registration'

    def send_email(self, to: str, subject: str, body: str) -> None:
        """
        Sends an email notification to the specified recipient.
        :param subject: The subject of the notification.
        :param body: The content or body of the email.
        :param to: The target recipient of the email.
        :return: None
        :raises Exception: Raised when there's an issue sending the email.
                """
        # Record the MIME types of both parts - text/plain and text/html.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg["From"] = formataddr((str(Header(self.SENDER_NAME, 'utf-8')), self.SENDER_ADDRESS))

        # Record the MIME types of both parts - text/plain and text/html.
        html_mime_text = MIMEText(body, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(html_mime_text)

        # Send email.
        # Details: http://www.samlogic.net/articles/smtp-commands-reference.htm
        try:
            self.service.sendmail(self.SENDER_ADDRESS, to, msg.as_string())
            self.service.close()
        except Exception:
            raise
