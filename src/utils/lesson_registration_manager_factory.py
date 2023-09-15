"""
Author: raviv steinberg
Date: 08/09/2023
"""
from src.common.holmes_place_api import HolmesPlaceAPI
from src.services.registration_params_service import RegistrationParamsService
from src.services.user_data_service import UserDataService
from src.utils.lesson_registration_manager import LessonRegistrationManager
from src.utils.lessons_manager import LessonsManager
from src.utils.yaml_handler import YAMLHandler


class LessonRegistrationManagerFactory:
    """
    A factory class for creating instances of the LessonRegistrationManager.
    The factory encapsulates the process of fetching user data, configuring the
    registration parameters, and setting up necessary dependencies.
    """

    def __init__(self, user_data_service: UserDataService, lesson_id: str):
        """
        Initializes the LessonRegistrationManagerFactory class.
        :param user_data_service: user data.
        :param lesson_id: str: ID of the lesson for which registration manager is required.
        """
        self.user_data_service = user_data_service
        self.lesson_id = lesson_id

    def get(self) -> LessonRegistrationManager:
        """
        Creates and returns an instance of LessonRegistrationManager by gathering all
        necessary parameters and setting up the required dependencies.
        :return: LessonRegistrationManager: Configured instance of the LessonRegistrationManager.
        """
        registration_params_service = RegistrationParamsService(club_id=self.user_data_service.club_id, lesson_id=self.lesson_id, lessons_manager=LessonsManager(), yaml_reader=YAMLHandler())
        params = registration_params_service.get_registration_params()
        return LessonRegistrationManager(
            user=self.user_data_service.user,
            password=self.user_data_service.password,
            lesson=params,
            api=HolmesPlaceAPI(),
            seats=self.__get_seats_by_lesson_id())

    def __get_seats_by_lesson_id(self) -> list:
        """
        Fetch the seats for a specific lesson_id.
        :return: list: A list of seat numbers as integers for the specified lesson_id.
        If lesson_id is not found, an empty list is returned.
        """
        for lesson in self.user_data_service.choices:
            if lesson['lesson_id'] == self.lesson_id:
                return [int(seat) for seat in lesson['seats'].split()]
        return []

