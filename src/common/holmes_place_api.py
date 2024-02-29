"""
Author: raviv steinberg
Date: 04/09/2023
"""
from requests import Response
from src.api.api_handler import ApiHandler
from src.utils.yaml_handler import YAMLHandler
from fake_useragent import UserAgent


class HolmesPlaceAPI:
    """
    A class to interact with Holmes Place API.
    This class provides methods for various operations like login, logout,
    getting available seats for a lesson, registering for a lesson, etc.

    Example Usage:
    api = HolmesPlaceAPI()
    api.login('username', 'password')
    seats = api.get_available_seats(params)
    """

    def __init__(self):
        """
        Initialize the API handler by reading configurations from the 'config.yaml'.
        """
        self.config = YAMLHandler.get_content(filepath='config.yaml')
        self.base_url = self.config['base_url']
        self.user_agent = UserAgent().random

    def login(self, user: str, password: str) -> Response:
        """
        Login to Holmes Place using provided credentials.
        :param user: str: The user's phone number or username.
        :param password: str: The user's password.
        """

        return ApiHandler.request(
            'POST',
            url=self.config['urls']['login'].format(base_url=self.base_url),
            data=f'phone={user}&password={password}',
            headers=self._get_headers())

    def logout(self) -> Response:
        """
        Logout from Holmes Place.
        """
        return ApiHandler.request(
            'POST',
            url=self.config['urls']['logout'].format(base_url=self.base_url),
            data='action=logout',
            headers={'content-type': 'text/html; charset=UTF-8'})

    def get_available_seats(self, params: dict) -> Response:
        """
        Get available seats for a lesson.
        :param params: dict: Parameters required to fetch available seats.
        :return: list: List of available seats.
        """
        return ApiHandler.request(
            'POST',
            url=self.config['urls']['available_seats'].format(base_url=self.base_url),
            data=f'branchID={params["club_id"]}&lessonID={params["lesson_id"]}&date={params["date"]}&time={params["start_time"]}',
            headers=self._get_headers())

    def register_lesson(self, params: dict):
        """
        Register for a lesson.
        :param params: dict: Parameters required to register for a lesson.
        """
        url = self.config['urls']['register_to_lesson'].format(base_url=self.base_url)
        data = f'branchID={params["lesson"]["club_id"]}&lessonID={params["lesson"]["id"]}&date={params["lesson"]["date"]}&time={params["lesson"]["start_time"]}&instructorID={params["instructor_id"]}'
        headers = self._get_headers()
        ApiHandler.request('POST', url, data=data, headers=headers)

    def register_lesson_with_seat(self, params: dict, seat: int) -> Response:
        """
        Register for a lesson with a specified seat.
        :param params: dict: Parameters required to register for a lesson with a specified seat.
        :param seat: int: The seat number that the user wishes to register for within the lesson.
        """
        return ApiHandler.request(
            'POST',
            url=self.config['urls']['register_to_lesson_with_seat'].format(base_url=self.base_url),
            data=f'branchID={params["club_id"]}&lessonID={params["lesson_id"]}&date={params["date"]}&time={params["start_time"]}&instructorID={params["instructor_id"]}&seatID={seat}',
            headers=self._get_headers())

    def register(self, user: str, birthday, password) -> Response:
        return ApiHandler.request(
            'POST',
            url=self.config['urls']['register'].format(base_url=self.base_url),
            data=f'phone={user}&password={password}&birthday={birthday}',
            headers={"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        )

    def _get_headers(self):
        """
        Get headers with a random User-Agent.
        :return: dict: Headers with a random User-Agent.
        """
        return {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': self.user_agent
        }
