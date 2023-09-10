"""
Author: raviv steinberg
Date: 04/09/2023
"""
import datetime


class DateUtils:
    """
    Utility class for date and time operations.
    Provides helper methods to perform various date and time related operations like getting the next specific weekday,
    converting a time string to a specific format, and more.
    """

    @staticmethod
    def next_weekday(date_time: datetime.date, weekday: str) -> datetime.date:
        """
        Get the next date for a given weekday from a specified date.
        :param date_time: datetime.date: The starting date.
        :param weekday: str: The desired weekday (e.g., 'monday', 'tuesday', ...).
        :return: datetime.date: The next date for the specified weekday.
        """
        days_ahead = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        }
        target_day = days_ahead[weekday.lower()]
        days_diff = (target_day - date_time.weekday() + 7) % 7
        return date_time + datetime.timedelta(days_diff)

    @staticmethod
    def format_time(time: str) -> str:
        """
        Convert a time from "HH:MM" format to "HHMM00" format.
        :param time: str: Time in "HH:MM" format.
        :return: str: Time in "HHMM00" format.
        """
        hours, minutes = time.split(':')
        return f'{hours.zfill(2)}{minutes.zfill(2)}00'

    @staticmethod
    def calculate_registration_time(lesson_day: str, lesson_time: str) -> datetime.datetime:
        """
        Calculate the registration time for a lesson based on its day and start time.
        The registration time is two days prior to the lesson day at the given lesson time.
        :param lesson_day: str: Day of the lesson (e.g., 'sunday', 'monday').
        :param lesson_time: str: Start time of the lesson (e.g., '7:30').
        :return: datetime.datetime: The registration datetime for the lesson.
        """
        # Determine the date of the next lesson.
        lesson_date = DateUtils.next_weekday(date_time=datetime.date.today(), weekday=lesson_day)
        hours, minutes = map(int, lesson_time.split(':'))
        lesson_datetime = datetime.datetime.combine(lesson_date, datetime.time(hour=hours, minute=minutes))

        # Subtract two days to get the registration date.
        return lesson_datetime - datetime.timedelta(days=2)

    @staticmethod
    def get_target_time(time: str, seconds_before: int) -> datetime.datetime:
        """
        Convert a time from "HHMMSS" format to a datetime object for the current day and subtracts the given seconds.
        :param time: str: Time in "HHMMSS" format.
        :param seconds_before: int: Number of seconds to subtract from the given time.
        :return: datetime.datetime: Target datetime object after subtracting seconds.
        """
        h, m, s = int(time[:2]), int(time[2:4]), int(time[4:])
        original_time = datetime.time(h, m, s)

        now = datetime.datetime.now()
        original_datetime = datetime.datetime.combine(now.date(), original_time)

        # Subtract given seconds
        return original_datetime - datetime.timedelta(seconds=seconds_before)