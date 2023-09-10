"""
Author: raviv steinberg
Date: 04/09/2023
"""
import json
import random
import time
from requests import Response
from src.common.holmes_place_api import HolmesPlaceAPI
from src.exceptions.bike_occupied_exception import BikeOccupiedException
from src.exceptions.lesson_not_open_for_registration import LessonNotOpenForRegistrationException
from src.exceptions.lesson_time_does_not_exist import LessonTimeDoesNotExistException
from src.exceptions.multiple_devices_connection_exception import MultipleDevicesConnectionException
from src.exceptions.no_available_seats_exception import NoAvailableSeatsException
from src.exceptions.no_matching_subscription import NoMatchingSubscriptionException
from src.exceptions.registration_for_this_lesson_already_exists import RegistrationForThisLessonAlreadyExistsException
from src.exceptions.registration_timeout_exception import RegistrationTimeoutException
from src.exceptions.user_preferred_seats_occupied_exception import UserPreferredSeatsOccupiedException
from src.utils.logger_manager import LoggerManager


class LessonRegistrationManager:
    def __init__(self, user: str, password: str, api: HolmesPlaceAPI, lesson: dict, seats: list[int]):
        """
        Initializes the LessonRegistrationManager instance.
        :param user: str: The username used for API interactions.
        :param password: str: The password corresponding to the provided username.
        :param api: HolmesPlaceAPI: An instance of the HolmesPlaceAPI to interact with the API endpoints.
        :param lesson: dict: Details of the lesson to be registered.
        :param seats: list[int]: Priority list of seat numbers the user wants to register with.
        """
        self.user = user
        self.password = password
        self.lesson = lesson
        self.api = api
        self._is_logged_in = False
        self.seats = seats
        self.__initialize_logger_manager()

    def register_lesson(self) -> None:
        """
        Registers the user for the specified lesson by either priority or random seat choice.
        :return: None
        """
        # self.login()
        # self.logger.info(f'lesson details: {self.lesson}')
        # self.logger.info(msg=f'User\'s preferred seats: {self.seats}')
        # seat = self.__get_first_priority_seat()
        # try:
        #     self.__wait_until_registration_starts(seat=seat)
        #     return
        # except BikeOccupiedException:
        #     self.logger.warning(msg=f'Preferred seat {seat} is occupied.')
        # except Exception as ex:
        #     raise ex
        # self.__register()
        self.__do_work()

    def login(self):
        """
        Logs the user into the system.
        :return: None
        """
        try:
            self.logger.debug(f'Attempting login for user: {self.user}.')
            self.api.login(user=self.user, password=self.password)
            self.logger.info(f'Successfully logged in as {self.user}.')
            self._is_logged_in = True
        except Exception as ex:
            self.__check_exception_message(error_msg=str(ex))
            raise

    def logout(self):
        """
        Logs out the user from the system.
        :return: None
        """
        if self._is_logged_in:
            self.logger.debug(f'Attempting logout for user: {self.user}.')
            time.sleep(5)
            self.api.logout()
            self._is_logged_in = False
            self.logger.info(f'Successfully logged out user: {self.user}.')

    def __do_work(self):
        try:
            self.login()
            self.logger.info(f'lesson details: {self.lesson}')
            self.logger.info(msg=f'User\'s preferred seats: {self.seats}')
            seat = self.__get_first_priority_seat()
            try:
                self.__wait_until_registration_starts(seat=seat)
                return
            except BikeOccupiedException:
                self.logger.warning(msg=f'Preferred seat {seat} is occupied.')
            except Exception as ex:
                raise ex
            self.__register()
        except Exception as ex:
            self.logger.exception(ex)
        finally:
            self.logout()

    def __wait_n_seconds_before_registration_start(self) -> None:
        pass

    def __register(self) -> bool:
        """
        Registers the user using their seat priority list.
        :return: bool: True if registration is successful, otherwise False.
        """
        self.logger.debug('Attempting registration with other priority seats.')
        while len(self.seats) > 0:
            seat = self.seats.pop(0)
            if self.__try_to_register_lesson(seat=seat):
                return True
        self.__register_by_random()

    def __get_first_priority_seat(self) -> int:
        """
        Get the first available priority seat for the user.
        :return: int: The seat number.
        """
        available_seats = self.__extract_available_seats(response=self.api.get_available_seats(params=self.lesson))
        try:
            self.__filter_priority_seats(available_seats=available_seats)
            seat = self.seats.pop(0)
        except UserPreferredSeatsOccupiedException:
            self.logger.warning(msg='All user\'s preferred seats are occupied. Selecting a random seat.')
            seat = self.__choose_random_seat(available_seats)
            self.logger.debug(f'Attempting registration with seat number: {seat}.')
        return seat

    def __initialize_logger_manager(self):
        # Initialize the LoggerManager for this instance
        logger_manager = LoggerManager(user=self.user)
        self.logger = logger_manager.logger

    def __register_by_random(self) -> None:
        """
        Registers the user by choosing a random seat.
        :return: None
        """
        self.logger.debug('Priority seats occupied, attempting random seat registration.')
        available_seats = self.__extract_available_seats(response=self.api.get_available_seats(params=self.lesson))
        self.logger.info('Selecting a random seat...')

        while len(available_seats) > 0:
            seat = self.__choose_random_seat(available_seats=available_seats)
            self.logger.debug(f'Attempting registration with seat number: {seat}.')
            if self.__try_to_register_lesson(seat=seat):
                return
            available_seats = self.__extract_available_seats(response=self.api.get_available_seats(params=self.lesson))
        raise Exception('Failed to register for the lesson.')

    def __wait_until_registration_starts(self, seat: int, timeout: int = 5) -> None:
        """
        Waits until the lesson registration begins.
        :param seat: int: The seat number to register with.
        :param timeout: int: Maximum wait time in minutes.
        :return: None
        """
        end_time = time.time() + timeout * 60
        self.logger.info(f'Waiting for \'{self.lesson["type"]}\' registration to start. Attempt to register for seat number {seat}.')

        while time.time() < end_time:
            try:
                self.__try_to_register_lesson(seat=seat)
                return
            except LessonNotOpenForRegistrationException as ex:
                self.logger.warning(ex)
            except LessonTimeDoesNotExistException:
                raise
            except RegistrationForThisLessonAlreadyExistsException:
                raise
            except NoMatchingSubscriptionException:
                raise
            except Exception as ex:
                self.logger.error(ex)
        self.logger.error(f'Could not register within {timeout} minute(s).')
        raise RegistrationTimeoutException(f'Could not register for lesson within {timeout} minute(s).')

    def __try_to_register_lesson(self, seat: int) -> bool:
        """
        Attempts to register the user for the lesson with the given seat.
        :param seat: int: Seat number.
        :return: bool: True if registration is successful, otherwise False.
        """
        try:
            self.api.register_lesson_with_seat(params=self.lesson, seat=seat)
            self.logger.info(msg=f'Successfully registered for \'{self.lesson["type"]}\' lesson with seat number {seat}.')
            return True
        except BikeOccupiedException as ex:
            self.logger.warning(ex)
        except Exception:
            raise

    def __extract_available_seats(self, response: Response) -> list[int]:
        """
        Extracts available seat numbers from the given API response.
        :param response: Response: The API response to extract seat numbers from.
        :return: list[int]: A list of available seat numbers.
        """
        data = response.json()
        if data.get("success"):
            available_seats = [int(seat) for seat in json.loads(data.get("availableSeats", "[]"))]
            if not available_seats:
                self.logger.error("No available seats retrieved from the response.")
                raise NoAvailableSeatsException
            self.logger.info(f'Available seats: {available_seats}.')
            return available_seats
        raise NoAvailableSeatsException

    def __filter_priority_seats(self, available_seats: list[int]) -> None:
        """
        Filters the user's priority seats based on the given list of available seats.
        :param available_seats: list[int]: The list of currently available seat numbers.
        :return: None
        """
        seats_before = len(self.seats)
        self.seats = [seat for seat in self.seats if seat in available_seats]
        seats_after = len(self.seats)
        if seats_after < seats_before:
            self.logger.warning(msg=f'{seats_before - seats_after} user\'s preferred seat(s) occupied.')
        if not self.seats:
            raise UserPreferredSeatsOccupiedException

    def __check_exception_message(self, error_msg: str) -> None:
        """
        Checks a given error message for specific conditions and raises exceptions accordingly.
        :param error_msg: str: The error message to be checked.
        :return: None
        """
        hebrew_message = "לא ניתן להתחבר עם אותו חשבון ממספר מכשירים"
        if error_msg == hebrew_message:
            self.logger.error("Cannot log in with the same account from multiple devices.")
            raise MultipleDevicesConnectionException()

    @staticmethod
    def __choose_random_seat(available_seats: list[int]) -> int:
        """
        Selects a random seat number from the given list of available seats.
        :param available_seats: list[int]: The list of available seat numbers.
        :return: int: A randomly selected seat number.
        """
        return random.choice(available_seats)
