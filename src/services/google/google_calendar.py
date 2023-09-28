import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from src.interfaces.google.icalendar_service import ICalendarService
from src.utils.project import Project
from typing import Any


class GoogleCalendar(ICalendarService):
    CREDENTIALS_FILE_NAME = 'credentials.json'
    TOKEN_NAME = 'calender_token.json'

    def __init__(self):
        """
        Initializes an instance of the GoogleCalendar class.
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
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(os.path.join(Project.root_path(),self.CREDENTIALS_FILE_NAME), self.get_scopes())
                credentials = flow.run_local_server(port=0)
            with open(self.TOKEN_NAME, 'w') as token:
                token.write(credentials.to_json())
        return build(serviceName='calendar', version='v3', credentials=credentials)

    def get_scopes(self) -> list:
        """
        Retrieves the list of scopes necessary for accessing the Google service.
        This method provides the OAuth 2.0 scopes required for authorization.
        These scopes determine the level of access the user grants to the application.
        :return: A list of strings, where each string is an OAuth 2.0 scope URL.
        """
        return ['https://www.googleapis.com/auth/calendar']

    def create_event(self, start_time: datetime, summary: str, description: str, duration: int, attendees: list, reminders: int = 60) -> str:
        """
        Creates an event on the primary Google Calendar and returns its link.
        :param start_time: A datetime representing the start of the event.
        :param summary: A string representing the summary of the event.
        :param description: A string representing the details of the event.
        :param duration: An integer representing the duration of the event in minutes.
        :param attendees: A list of email addresses to be added as attendees.
        :param reminders: An integer representing the number of minutes before
        the event starts to send a reminder. Default is 60 minutes.
        :return: A string containing the link to the created event.
        """
        # end_time = start_time + datetime.timedelta(minutes=duration)
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Jerusalem',
            },
            'end': {
                'dateTime': (start_time + datetime.timedelta(minutes=duration)).isoformat(),
                'timeZone': 'Asia/Jerusalem',
            },
            'colorId': '1',
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': reminders},
                    {'method': 'email', 'minutes': reminders}
                ]
            },
            'attendees': [{'email': email} for email in attendees]
        }

        created_event = self.service.events().insert(calendarId='primary', body=event).execute()
        return created_event['htmlLink']
