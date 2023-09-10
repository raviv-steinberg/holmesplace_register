"""
Author: raviv steinberg
Date: 08/09/2023
"""
from src.common.holmes_place_api import HolmesPlaceAPI
from src.services.registration_params_service import RegistrationParamsService
from src.utils.lesson_registration_manager import LessonRegistrationManager
from src.utils.lessons_manager import LessonsManager
from src.utils.logger_manager import LoggerManager
from src.utils.yaml_reader import YAMLReader


class LessonRegistrationManagerFactory:
    """
    A factory class for creating instances of the LessonRegistrationManager.
    The factory encapsulates the process of fetching user data, configuring the
    registration parameters, and setting up necessary dependencies.
    """

    def __init__(self, source_user_data_file: str, lesson_id: str):
        """
        Initializes the LessonRegistrationManagerFactory class.
        :param source_user_data_file: str: Path to the YAML file containing user's data.
        :param lesson_id: str: ID of the lesson for which registration manager is required.
        """
        self.source_user_data_file = source_user_data_file
        self.lesson_id = lesson_id

    def get(self) -> LessonRegistrationManager:
        """
        Creates and returns an instance of LessonRegistrationManager by gathering all
        necessary parameters and setting up the required dependencies.
        :return: LessonRegistrationManager: Configured instance of the LessonRegistrationManager.
        """
        user_data = self.__read_user_data()
        registration_params_service = RegistrationParamsService(source_user_data_file=self.source_user_data_file, lesson_id=self.lesson_id, lessons_manager=LessonsManager(), yaml_reader=YAMLReader())
        params = registration_params_service.get_registration_params()
        return LessonRegistrationManager(
            user=user_data['user'],
            password=user_data['password'],
            lesson=params,
            api=HolmesPlaceAPI(),
            seats=self.__parse_seats_list(user_data=user_data))

    def __parse_seats_list(self, user_data: dict) -> list:
        """
        Extracts and parses the 'seats' data for the given lesson ID from the user's data.
        If 'seats' contains integer data, it is returned as a single-element list.
        If 'seats' contains a space-separated string, it is split into individual seat numbers and returned as a list.
        In case of missing or malformed data, an empty list is returned.
        :param user_data: dict: The user data dictionary.
        :return: list[int]: A list of seat numbers.
        """
        try:
            seats_data = next((lesson['seats'] for lesson in user_data['user_schedule'] if lesson['lesson_id'] == self.lesson_id), None)
            if not seats_data:
                return []
            return [seats_data] if isinstance(seats_data, int) else [int(seat) for seat in seats_data.split()]
        except KeyError:
            return []

    def __log_lesson_params(self, d, indent=0):
        """
        Recursively formats a dictionary into a human-readable multi-line string. This function
        is mainly intended for debugging and logging purposes, providing a clear view of nested dictionary content.
        :param d: dict: Dictionary to format.
        :param indent: int: Current indentation level. (used for recursive calls, not set by the caller)
        :return: str: Formatted multi-line string representation of the dictionary.
        """
        items = []
        for key, value in d.items():
            if isinstance(value, dict):
                items.append('  ' * indent + str(key) + ': ' + self.__log_lesson_params(value, indent + 1))
            elif isinstance(value, list):
                list_items = ['\n' + '  ' * (indent + 1) + '- ' + str(item) for item in value]
                items.append('  ' * indent + str(key) + ': [' + ','.join(list_items) + '\n' + '  ' * indent + ']')
            else:
                items.append('  ' * indent + str(key) + ': ' + str(value))
        return '\n' + ',\n'.join(items) + '\n' + '  ' * (indent - 1)

    def __read_user_data(self) -> dict:
        """
        Reads and returns user data from the source YAML file.
        :return: dict: Parsed content of the user data file.
        """
        return YAMLReader.get_content(filepath=self.source_user_data_file)
