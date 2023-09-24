import base64
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.utils.project import Project


class GoogleCalendarOld:
    """
    A class to interact with the Google Calendar API.
    """

    def __init__(self):
        """
        Initializes an instance of the GoogleCalendar class.
        """
        self.service = self.authenticate()
        self.service2 = self.authenticate2()

    def authenticate(self):
        """
        Authenticates the user and returns the service for Google Calendar API.
        :return: An authenticated service for Google Calendar API.
        """
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        if os.path.exists('calender_token.json'):
            creds = Credentials.from_authorized_user_file('calender_token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(os.path.join(Project.root_path(), 'src', 'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            with open('calender_token.json', 'w') as token:
                token.write(creds.to_json())
        return build('calendar', 'v3', credentials=creds)

    def create_event(self, start_time: datetime, summary: str, description: str, duration: int, attendees: list):
        """
        Creates an event on the primary Google Calendar.
        :param start_time: A datetime representing the start of the event.
        :param summary: A string representing the summary of the event.
        :param description: A string representing the details of the event.
        :param duration: An integer representing the duration of the event in minutes.
        :param attendees: list: A list of email addresses to be added as attendees
        """
        end_time = start_time + datetime.timedelta(minutes=duration)
        attendees_list = [{'email': email} for email in attendees]

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Jerusalem',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Jerusalem',
            },
            'colorId': '1',
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},
                    {'method': 'email', 'minutes': 60}
                ]
            },
            'attendees': attendees_list
        }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event['htmlLink']}")

    def authenticate2(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        creds = None
        if os.path.exists('token_gmail.json'):  # Use a different token file for Gmail to avoid conflicts
            creds = Credentials.from_authorized_user_file('token_gmail.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(os.path.join(Project.root_path(), 'src', 'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token_gmail.json', 'w') as token:  # Use a different token file for Gmail
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)  # Use 'gmail' and 'v1' for the Gmail API

    def send_email(self, to_email: str, subject: str, body: str):
        """
        Sends an email using the Gmail API.
        :param to_email: The recipient email address.
        :param subject: The email subject.
        :param body: The email body.
        """
        # Create a MIMEText message.
        from email.mime.text import MIMEText
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject

        # Convert the message to raw bytes (base64 encoded string).
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        try:
            sent_message = self.service2.users().messages().send(userId='me', body={'raw': raw_message}).execute()
            print(f"Message sent (ID: {sent_message['id']})")
        except HttpError as error:
            print(f"An error occurred: {error}")