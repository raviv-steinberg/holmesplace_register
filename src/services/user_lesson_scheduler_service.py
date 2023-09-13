"""
Author: raviv steinberg
Date: 06/09/2023
"""
import time
from datetime import datetime, timedelta
from src.utils.lessons_manager import LessonsManager
from src.utils.yaml_reader import YAMLReader


class UserLessonSchedulerService:
    """
    Service class for managing user lesson schedules.
    This class helps to fetch user's choice of lessons and
    calculate the time remaining for each lesson's registration.
    """
    WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    def __init__(self, source_user_data_file: str):
        """
        Initializes the UserLessonScheduler class.
        :param source_user_data_file: str: Path to the YAML file containing user's lesson schedule.
        """
        self.secure_user_data_file = source_user_data_file
        self.choices = None
        self.club_id = None
        self.lessons_manager = LessonsManager()

    def __read_user_choices(self) -> None:
        """
        Private method to fetch user's club_id & lesson choices from the provided YAML file.
        :return: None.
        """
        data = YAMLReader.get_content(filepath=self.secure_user_data_file)
        self.choices = data['user_schedule']
        self.club_id = data['club_id']

    @staticmethod
    def __format_minutes_to_seconds(minutes_float: float) -> int:
        """
        Converts a given value in minutes (as a float) to its equivalent in seconds (as an integer).
        :param minutes_float: float: Number of minutes.
        :return: Equivalent value in seconds.
        """
        return int(minutes_float * 60)

    def get_upcoming_lessons(self) -> list[tuple]:
        """
        Fetches upcoming lessons based on the user's choices and calculates time until the registration for each lesson.
        :return: List of tuples where each tuple consists of a lesson ID and the time in minutes until its registration.
        """
        self.__read_user_choices()
        all_lessons = self.lessons_manager.get_all(club_id=self.club_id)

        upcoming_lessons = []

        for user_choice in self.choices:
            lesson_id = user_choice['lesson_id']

            for category, lessons in all_lessons.items():
                for lesson in lessons:
                    if lesson["lesson_id"] == lesson_id:
                        reg_day = lesson["registration_day"]
                        reg_time = datetime.strptime(lesson["registration_start_time"], "%H:%M").time()
                        time_until_reg = self.__calculate_time_until(reg_day, reg_time)
                        upcoming_lessons.append((lesson_id, time_until_reg))
                        break
        return upcoming_lessons

    def monitor_registration_time(self, threshold_minutes: int = 3) -> tuple:
        """
        Continuously monitors the closest lesson registration time.
        Whenever a lesson's registration time is found to be a specific number of minutes away (default 3 minutes),
        it returns that lesson's ID.
        :param threshold_minutes: The number of minutes away from registration to trigger an alert and return the lesson ID.
        :return: A tuple containing the lesson's ID and the time remaining until registration (in minutes).
        Returns (None, None) if no lesson meets the criteria.
        """
        return next((lesson_tuple for lesson_tuple in self.get_upcoming_lessons() if lesson_tuple[1] <= threshold_minutes), (None, None))

    def __calculate_time_until(self, registration_day: str, registration_time: time) -> float:
        """
        Private method to calculate time in minutes from now until the specified day and time.
        :param registration_day: str: The day of registration.
        :param registration_time: time: The time of registration on the specified day.
        :return: Time in minutes from now until the specified registration day and time.
        """
        now = datetime.now()
        target_weekday = self.WEEKDAYS.index(registration_day)

        # Calculate the difference in days to the target weekday.
        days_difference = (target_weekday - now.weekday() + 7) % 7
        target_datetime = now + timedelta(days=days_difference)

        # Combine the target date with the registration time.
        target_datetime = target_datetime.replace(hour=registration_time.hour, minute=registration_time.minute, second=0, microsecond=0)

        # The target time has already passed for this week; calculate for next week.
        if target_datetime < now:
            target_datetime += timedelta(days=7)

        # Return difference in minutes.
        time_diff = target_datetime - now
        return time_diff.total_seconds() / 60
