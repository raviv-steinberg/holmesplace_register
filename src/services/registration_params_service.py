"""
Author: raviv steinberg
Date: 08/09/2023
"""
import datetime
from src.utils.date_utils import DateUtils
from src.utils.lessons_manager import LessonsManager
from src.utils.yaml_reader import YAMLReader


class RegistrationParamsService:
    """
    This service provides methods to obtain registration parameters
    based on the user's data and lesson details.
    """

    def __init__(self, source_user_data_file: str, lesson_id, lessons_manager: LessonsManager, yaml_reader: YAMLReader):
        """
        Initializes the RegistrationParamsService class.
        :param source_user_data_file: str: Path to the YAML file containing user's data.
        :param lesson_id: str: ID of the lesson for which parameters are required.
        :param lessons_manager: LessonsManager: Manages and retrieves lessons data.
        :param yaml_reader: YAMLReader: Reads and returns data from a given YAML file.
        """
        self.source_user_data_file = source_user_data_file
        self.lesson_id = lesson_id
        self.lessons_manager = lessons_manager
        self.yaml_reader = yaml_reader

    def get_registration_params(self) -> dict:
        """
        Determines and returns the registration parameters for the given lesson.
        :return: dict: Registration parameters including club ID, lesson ID, date, start time, and instructor ID.
        """
        user_data = self.yaml_reader.get_content(filepath=self.source_user_data_file)
        lesson = self.lessons_manager.retrieve_lesson_details(lesson_id=self.lesson_id)
        params = dict()
        params['type'] = lesson['type']
        params['club_id'] = user_data['club_id']
        params['lesson_id'] = self.lesson_id
        params['date'] = DateUtils.next_weekday(date_time=datetime.date.today(), weekday=lesson['day']).strftime('%Y/%m/%d')
        params['start_time'] = DateUtils.format_time(time=lesson['start_time'])
        params['instructor_id'] = lesson['instructor_id']
        return params
