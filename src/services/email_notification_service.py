import smtplib
from src.interfaces.inotification import INotification
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


class EmailNotificationService(INotification):
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
    SMTP_SERVER_ADDRESS = 'smtp.gmail.com'
    SMTP_SERVER_PORT = 465
    SENDER_ADDRESS = 'yad2reporter@gmail.com'
    SENDER_PASSWORD = 'jnsykynsmmefjrzy'
    SENDER_NAME = 'Mishka\'s amazing robot'

    def send(self, subject: str, message: str, recipient: str) -> None:
        """
        Sends an email notification to the specified recipient.
        :param subject: The subject of the notification.
        :param message: The content or body of the email.
        :param recipient: The target recipient of the email.
        :return: None
        :raises Exception: Raised when there's an issue sending the email.
        """
        # Record the MIME types of both parts - text/plain and text/html.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg["From"] = formataddr((str(Header(self.SENDER_NAME, 'utf-8')), self.SENDER_ADDRESS))

        # Record the MIME types of both parts - text/plain and text/html.
        html_mime_text = MIMEText(message, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(html_mime_text)

        # Send email.
        # Details: http://www.samlogic.net/articles/smtp-commands-reference.htm
        try:
            server = smtplib.SMTP_SSL(self.SMTP_SERVER_ADDRESS, self.SMTP_SERVER_PORT)
            server.ehlo()
            server.login(self.SENDER_ADDRESS, self.SENDER_PASSWORD)
            server.sendmail(self.SENDER_ADDRESS, recipient, msg.as_string())
            server.close()
        except Exception:
            raise
