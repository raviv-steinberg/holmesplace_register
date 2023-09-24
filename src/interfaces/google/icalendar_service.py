from abc import abstractmethod
from datetime import datetime
from src.interfaces.google.igoogle_service import IGoogleService


class ICalendarService(IGoogleService):
    """
    Abstract base class for calendar services.
    """
    @abstractmethod
    def create_event(self, start_time: datetime, summary: str, description: str, duration: int, attendees: list) -> str:
        """
        Creates an event on the primary Google Calendar and returns its link.
        :param start_time: A datetime representing the start of the event.
        :param summary: A string representing the summary of the event.
        :param description: A string representing the details of the event.
        :param duration: An integer representing the duration of the event in minutes.
        :param attendees: A list of email addresses to be added as attendees.
        :return: A string containing the link to the created event.
        """
        raise NotImplementedError
