"""
Author: raviv steinberg
Date: 04/09/2023
"""
from src.exceptions.lesson_not_found_exception import LessonNotFoundException
from src.utils.lessons_loader import LessonsLoader


class LessonsManager:
    """
    Manager class to read and handle the lessons from project holmes_lessons.yaml file.
    """
    def __init__(self,):
        """
        Initializes the LessonsManager class.
        Default is 'holmes_lessons.yaml' in the root directory.
        """
        self.loader = LessonsLoader()
        self.lessons = self.loader.lessons

    def get_all(self, club_id:int):
        return self.lessons['clubs'][club_id]

    def get_lesson(self, club_id: int, lesson_type: str, day_of_week: str, time: str) -> dict:
        """
        Retrieves lesson registration params details based on club ID, lesson type, day of the week, and time.
        :param club_id: int: Club ID (e.g., 205).
        :param lesson_type: str: Type of the lesson (e.g., 'pilates', 'spinning').
        :param day_of_week: str: Day of the week (e.g., 'sunday', 'monday').
        :param time: str: Start time of the lesson in "HH:MM" format  (e.g., '7:30').
        :return: dict: A dictionary containing the details of the matched lesson.
        """
        club_data = self.lessons['clubs'][club_id]
        for lesson in club_data.get(lesson_type, []):
            if lesson['day'] == day_of_week and lesson['start_time'] == time:
                return lesson
        raise LessonNotFoundException(lesson_type=lesson_type, club_id=club_id, day_of_week=day_of_week, time=time)

    def retrieve_lesson_details(self, lesson_id: str) -> dict:
        """
        Retrieve lesson details based on the given lesson_id.
        :param lesson_id: str: The lesson ID to search for.
        :return: dict or None: The lesson details if found, otherwise None.
        """
        for club_id, club_data in self.lessons['clubs'].items():
            for lesson_type, lessons in club_data.items():
                for lesson in lessons:
                    if lesson['lesson_id'] == lesson_id:
                        return lesson
        raise LessonNotFoundException(lesson_id=lesson_id)
