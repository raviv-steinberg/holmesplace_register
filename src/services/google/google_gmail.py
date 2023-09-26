import base64
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from src.interfaces.google.iemail_service import IEmailService
from googleapiclient.discovery import build
from src.utils.project import Project
from typing import Any


class GoogleGmail(IEmailService):
    CREDENTIALS_FILE_NAME = 'credentials.json'
    TOKEN_NAME = 'gmail_token.json'

    def __init__(self):
        """
        Initializes an instance of the GoogleGmail class.
        """
        self.service = self.authenticate()

    def authenticate(self) -> Any:
        """
        Authenticates the user and returns the service for a specific Google API.
        :return: An authenticated service for Google Calendar API.
        """
        credentials = None
        if os.path.exists(self.TOKEN_NAME):
            credentials = Credentials.from_authorized_user_file(self.TOKEN_NAME, self.get_scopes())
        if not credentials or not credentials.valid:
            print(credentials.token_uri)
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(os.path.join(Project.root_path(), self.CREDENTIALS_FILE_NAME), self.get_scopes())
                credentials = flow.run_local_server(port=0)
            with open(self.TOKEN_NAME, 'w') as token:
                token.write(credentials.to_json())
        return build('gmail', 'v1', credentials=credentials)

    def get_scopes(self) -> list:
        """
        Retrieves the list of scopes necessary for sending emails via the Gmail API.
        This method provides the OAuth 2.0 scopes required for authorization.
        These scopes determine the level of access the user grants to the application
        for sending emails on their behalf.
        :return: A list of strings, where each string is an OAuth 2.0 scope URL.
        """
        return ['https://www.googleapis.com/auth/gmail.send']

    def send_email(self, to: str, subject: str, body: str) -> None:
        """
        Sends an email using the Gmail API.
        :param to: The recipient email address.
        :param subject: The email subject.
        :param body: The email body.
        :return: None
        """
        # Create a MIMEText message.
        from email.mime.text import MIMEText
        message = MIMEText(body, 'html')
        message['to'] = to
        message['subject'] = subject

        # Convert the message to raw bytes (base64 encoded string).
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        try:
            sent_message = self.service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
            print(f"Message sent (ID: {sent_message['id']})")
        except HttpError:
            raise
