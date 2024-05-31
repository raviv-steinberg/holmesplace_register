"""
Author: raviv steinberg
Date: 04/09/2023
"""
import json
import random
import time
import pause
import requests
from src.common.holmes_place_api import HolmesPlaceAPI
from src.enums.days_of_week import DaysOfWeek
from src.enums.lesson_type import LessonType
from src.exceptions.bike_occupied_exception import BikeOccupiedException
from src.exceptions.lesson_canceled_exception import LessonCanceledException
from src.exceptions.lesson_not_found_exception import LessonNotFoundException
from src.exceptions.lesson_not_open_for_registration import LessonNotOpenForRegistrationException
from src.exceptions.lesson_time_does_not_exist import LessonTimeDoesNotExistException
from src.exceptions.multiple_devices_connection_exception import MultipleDevicesConnectionException
from src.exceptions.no_available_seats_exception import NoAvailableSeatsException
from src.exceptions.no_matching_subscription import NoMatchingSubscriptionException
from src.exceptions.registration_for_this_lesson_already_exists import RegistrationForThisLessonAlreadyExistsException
from src.exceptions.registration_timeout_exception import RegistrationTimeoutException
from src.exceptions.user_preferred_seats_occupied_exception import UserPreferredSeatsOccupiedException
from src.interfaces.inotification import INotification
from src.services.email.email_preparer_service import EmailPreparerService
# from src.services.google.google_calendar import GoogleCalendar
# from src.services.google.google_gmail import GoogleGmail
from src.services.smtp_service import SMTPService
from src.services.user_data_service import UserDataService
from src.services.whatsapp.whatsapp_service import WhatsappService
from src.utils.date_utils import DateUtils
from src.utils.logger_manager import LoggerManager


class LessonRegistrationManager:
    """
    The LessonRegistrationManager manages the process of registering a user for a specific lesson.
    The manager interacts with the HolmesPlaceAPI to log in, retrieve available seats, and perform registration.
    It prioritizes user-preferred seats, but if they are occupied, it attempts to register the user on a random seat.
    """

    def __init__(self, user_data_service: UserDataService, api: HolmesPlaceAPI, lesson: dict, seats: list[int],
                 notifier: INotification = None):
        """
        Initializes the LessonRegistrationManager instance.
        :param user_data_service: user data.
        :param api: HolmesPlaceAPI: An instance of the HolmesPlaceAPI to interact with the API endpoints.
        :param lesson: dict: Details of the lesson to be registered.
        :param seats: list[int]: Priority list of seat numbers the user wants to register with.
        :param notifier: An instance of a class that implements the INotification interface.
        This is used to send notifications regarding the registration process.
        """
        self.__validate_input(lesson=lesson, seats=seats)
        self.user_data_service = user_data_service
        self.lesson = lesson
        self.api = api
        self._is_logged_in = False
        self.seats = seats
        self.__initialize_logger_manager()
        self.notifier = notifier

    def __repr__(self):
        return f'Start the registration process for the \'{self.lesson["type"].upper()}\' lesson' \
               f' on {self.lesson["day"].upper()}, {self.lesson["date"]} at {DateUtils.convert_time_format(time_str=self.lesson["start_time"])}'

    @staticmethod
    def __validate_input(lesson: dict, seats: list[int]) -> None:
        """
        Validates the input parameters for the LessonRegistrationManager.
        This function checks:
        - if the `lesson` dictionary is not empty or None.
        - if the `seats` list is not empty or None.
        :param lesson: dict: Details of the lesson to be registered.
        :param seats: list[int]: Priority list of seat numbers the user wants to register with.
        :raises ValueError: If any of the input parameters are invalid.
        """
        if not lesson:
            raise ValueError('[LessonRegistrationManager] - Invalid lesson.')
        if not seats:
            raise ValueError('[LessonRegistrationManager] - Invalid seats.')

    def register_lesson(self) -> str:
        """
        Registers the user for the specified lesson by either priority or random seat choice.
        :return: None
        """
        if self.user_data_service.notify_start_running:
            self.logger.debug(
                msg=f'user\'s notify start running value is '
                    f'{self.user_data_service.notify_start_running}, '
                    f'Send an email')
            SMTPService().send_email(
                to=self.user_data_service.email,
                subject=self.__get_email_start_running_subject(),
                body=self.__get_email_start_running_body())
        else:
            self.logger.debug(
                msg=f'user\'s notify start_running value is '
                    f'{self.user_data_service.notify_start_running}, '
                    f'An email will not be sent')

        self.logger.info(self)
        return str(self.__do_work())

    def login(self):
        """
        Logs the user into the system.
        :return: None
        """
        try:
            self.logger.debug(f'Attempting login for user: {self.user_data_service.user}.')
            self.api.login(user=self.user_data_service.user, password=self.user_data_service.password)
            self.logger.info(f'Successfully logged in as {self.user_data_service.user}.')
            self._is_logged_in = True
        except Exception as ex:
            LessonRegistrationManager.__check_exception_message(error_msg=str(ex))
            raise

    def logout(self):
        """
        Logs out the user from the system.
        :return: None
        """
        time.sleep(2)
        self.api.logout()
        self._is_logged_in = False
        self.logger.info(f'User \'{self.user_data_service.user}\' successfully logged out.')

    def __send_remainder(self, seat: int):
        try:
            subject, body = EmailPreparerService().prepare_email(attendee_name=self.user_data_service.name,
                                                                 lesson=self.lesson, seat=seat)
            SMTPService().send_email(to=self.user_data_service.email, subject=subject, body=body)

            # Send whatsapp message.
            self.logger.debug(msg=f'User whatsapp_group_name: {self.user_data_service.whatsapp_group_name}')
            if self.user_data_service.whatsapp_group_name:
                self.logger.info(msg=f'Notify running by Whatsapp to {self.user_data_service.whatsapp_group_name}')
                messages = [
                    f'הרישום לשיעור {LessonType.get_hebrew_name(english_name=self.lesson["type"].upper())} בוצע בהצלחה! 🎉',
                    f'',
                    f'פרטי השיעור:',
                    f'יום: {DaysOfWeek.get_hebrew_day(self.lesson["day"].upper())}',
                    f'תאריך: {"/".join(self.lesson["date"].split("/")[::-1])}',
                    f'שעה: {DateUtils.convert_time_format(time_str=self.lesson["start_time"])}',
                    f'מקום מספר: *{seat}*',
                    f'',
                    'נשמח לראותך בשיעור! 💪']

                WhatsappService(logger=self.logger).send_message(
                    contact_name=self.user_data_service.whatsapp_group_name,
                    message='\n'.join(messages))

            # try:
            #     GoogleGmail().send_email(to=self.user_data_service.email, subject=subject, body=body)
            # except Exception as ex:
            #     self.logger.error(ex)
            #     SMTPService().send_email(to=self.user_data_service.email, subject=subject, body=body)
            # try:
            #     GoogleCalendar().create_event(
            #         start_time=datetime.strptime(f'{self.lesson["date"]} {DateUtils.convert_time_format(time_str=self.lesson["start_time"])}', '%Y/%m/%d %H:%M'),
            #         summary=f'{self.lesson["type"].upper()} at {DateUtils.convert_time_format(time_str=self.lesson["start_time"])}, seat number {seat}',
            #         description='',
            #         duration=60,
            #         attendees=[self.user_data_service.email])
            # except Exception as ex:
            #     self.logger.error(ex)
        except Exception as ex:
            self.logger.exception(ex)

    def __do_work(self):
        """
        Handles the process of user registration for a lesson. This includes:
        - Logging in.
        - Setting the registration progress.
        - Waiting until the specified registration start time.
        - Checking for seat availability.
        - Registering for the lesson.
        Exceptions related to lessons and registration are logged for troubleshooting. After the process, the user is logged out.
        :return: None
        """
        try:
            self.__handle_registration_process()
            try:
                seat = self.__wait_before_registration_start()
            except BikeOccupiedException:
                seat = self.__register()
            if seat:
                if self.user_data_service.notify_result:
                    self.logger.debug(
                        msg=f'user\'s notify result value is {self.user_data_service.notify_result}, Send an email')
                    self.__send_remainder(seat=seat)
                else:
                    self.logger.debug(
                        msg=f'user\'s notify result value is {self.user_data_service.notify_result}, An email will not be sent')
                return seat
        except (LessonNotFoundException, LessonNotOpenForRegistrationException, LessonTimeDoesNotExistException,
                MultipleDevicesConnectionException, NoAvailableSeatsException, NoMatchingSubscriptionException,
                LessonCanceledException,
                RegistrationForThisLessonAlreadyExistsException, RegistrationTimeoutException,
                UserPreferredSeatsOccupiedException) as ex:
            self.logger.error(ex)
            return ex
        except Exception as ex:
            self.logger.exception(ex)
        finally:
            self.user_data_service.set_registration_progress(lesson_id=self.lesson['lesson_id'], in_progress=False)
            self.logout()

    def __handle_registration_process(self):
        """
        Prepares and initiates the registration process.
        This function:
        1. Logs into the system.
        2. Sets the registration progress for the given lesson.
        3. Waits until a specified time before registration starts.
        4. Logs lesson details and user's preferred seats.
        :return: None
        """
        self.login()
        self.user_data_service.set_registration_progress(lesson_id=self.lesson['lesson_id'], in_progress=True)
        self.__wait_n_seconds_before_registration_start()
        self.logger.info(f'lesson details: {self.lesson}')
        self.logger.info(msg=f'User\'s preferred seats: {self.seats}')

    def __wait_before_registration_start(self) -> int:
        """
            Waits until the registration process starts.
            This function checks the availability of the first priority seat for the user.
            It waits until the registration starts. If the first priority seat is occupied
            or any other exception occurs, it logs a warning or raises the exception, respectively.
            :return: Registered seat numer.
            :raises BikeOccupiedException: If the preferred seat is occupied.
            :raises Exception: For any other unexpected issues.
            """
        seat = self.__get_first_priority_seat()
        try:
            self.__wait_until_registration_starts(seat=seat)
            return seat
        except Exception:
            raise

    def __wait_n_seconds_before_registration_start(self, seconds_before: int = 2) -> None:
        """
        Waits for a specified number of seconds before the lesson's registration start time.
        :param seconds_before: The number of seconds to wait before the lesson's registration starts. Default is 30 seconds.
        :return: None
        """
        self.logger.debug(
            msg=f'\'{self.lesson["type"]}\' registration start time: {self.lesson["registration_start_time"]}.')
        target = DateUtils.get_target_time(time=self.lesson['registration_start_time'], seconds_before=seconds_before)
        self.logger.debug(msg=f'Pausing until {target} ({seconds_before} seconds before registration starts).')
        pause.until(time=target)
        self.logger.debug(msg=f'Resumed execution. Current time: {DateUtils.current_time()}')

    def __register(self) -> int:
        """
        Registers the user using their seat priority list.
        :return: Registered seat numer.
        """
        self.logger.debug('Attempting registration with other priority seats.')
        while len(self.seats) > 0:
            try:
                seat = self.seats.pop(0)
                if self.__try_to_register_lesson(seat=seat):
                    return seat
            except Exception as ex:
                self.logger.error(ex)
        seat = self.__register_by_random()
        if seat:
            return seat

    def __get_first_priority_seat(self) -> int:
        """
        Get the first available priority seat for the user.
        :return: int: The seat number.
        """
        available_seats = self.__extract_available_seats()
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
        logger_manager = LoggerManager(user=self.user_data_service.user)
        self.logger = logger_manager.logger

    def __register_by_random(self) -> int:
        """
        Registers the user by choosing a random seat.
        :return: Registered seat numer.
        """
        self.logger.debug('Priority seats occupied, attempting random seat registration.')
        available_seats = self.__extract_available_seats()
        self.logger.info('Selecting a random seat...')

        while len(available_seats) > 0:
            seat = self.__choose_random_seat(available_seats=available_seats)
            self.logger.debug(f'Attempting registration with seat number: {seat}.')
            if self.__try_to_register_lesson(seat=seat):
                return seat
            available_seats = self.__extract_available_seats()
        raise Exception('Failed to register for the lesson.')

    def __wait_until_registration_starts(self, seat: int, timeout: int = 3) -> None:
        """
        Waits until the lesson registration begins.
        :param seat: int: The seat number to register with.
        :param timeout: int: Maximum wait time in minutes.
        :return: None
        """
        end_time = time.time() + timeout * 60
        self.logger.info(
            f'Waiting for \'{self.lesson["type"]}\' registration to start. Attempt to register for seat number {seat}.')

        while time.time() < end_time:
            try:
                self.__try_to_register_lesson(seat=seat)
                return
            except LessonNotOpenForRegistrationException as ex:
                self.logger.warning(ex)
                time.sleep(1)
            except (
                    BikeOccupiedException, LessonTimeDoesNotExistException,
                    RegistrationForThisLessonAlreadyExistsException,
                    NoMatchingSubscriptionException, LessonCanceledException):
                raise
            except requests.exceptions.HTTPError as ex:
                self.logger.error(ex)
                time.sleep(2)
            except Exception as ex:
                self.logger.error(ex)
        raise RegistrationTimeoutException(
            f'Failed to register for lesson \'{self.lesson["type"]}\'  within {timeout} minute(s).')

    def __try_to_register_lesson(self, seat: int) -> bool:
        """
        Attempts to register the user for the lesson with the given seat.
        :param seat: int: Seat number.
        :return: bool: True if registration is successful, otherwise False.
        """
        try:
            self.api.register_lesson_with_seat(params=self.lesson, seat=seat)
            self.logger.info(
                msg=f'Successfully registered for \'{self.lesson["type"]}\' lesson with seat number {seat}.')
            return True
        except BikeOccupiedException as ex:
            self.logger.warning(ex)
            raise
        except Exception:
            raise

    def __extract_available_seats(self, retries: int = 5, delay: int = 1) -> list[int]:
        """
        Extracts available seat numbers from the given API response.
        :param retries: int: Number of retries in case of failure. Default is 5.
        :param delay: int: Delay between retries in seconds. Default is 1 second.
        :return: list[int]: A list of available seat numbers.
        """
        self.logger.debug(msg=f'Extract available seats for \'{self.lesson["type"]}\' lesson')
        for attempt in range(retries):
            self.logger.debug(msg=f'Attempt {attempt + 1} of {retries}')
            try:
                response = self.api.get_available_seats(params=self.lesson)
                data = response.json()
                if data.get('success'):
                    available_seats = [int(seat) for seat in json.loads(data.get('availableSeats', '[]'))]
                    if not available_seats:
                        self.logger.error('No available seats retrieved from the response.')
                        raise NoAvailableSeatsException
                    self.logger.info(f'Available seats: {available_seats}.')
                    return available_seats
                raise NoAvailableSeatsException
            except NoAvailableSeatsException as ex:
                self.logger.error(msg=f'{ex}. Retrying...')
            except Exception as ex:
                self.logger.error(msg=ex)

            self.logger.debug(msg=f'Sleep {delay} second(s) and retry...')
            time.sleep(delay)
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

    def __get_email_start_running_subject(self) -> str:
        """
        Get subject of start running message.
        :return: String representation of stat running message.
        """
        return f'🤖 {self.lesson["type"].upper()} Robot Starts Running!'

    def __get_email_start_running_body(self) -> str:
        """
        Get subject of start running message.
        :return: String representation of stat running message.
        """
        preferred_seats = ', '.join(str(x) for x in self.seats)
        return f'{self.lesson["type"].upper()} lesson' \
               f' on {self.lesson["day"].upper()}, {self.lesson["date"]}' \
               f' at {DateUtils.convert_time_format(time_str=self.lesson["start_time"])} <br>' \
               f'Preferred seats: {preferred_seats}'

    @staticmethod
    def __check_exception_message(error_msg: str) -> None:
        """
        Checks a given error message for specific conditions and raises exceptions accordingly.
        :param error_msg: str: The error message to be checked.
        :return: None
        """
        hebrew_message = "לא ניתן להתחבר עם אותו חשבון ממספר מכשירים"
        if error_msg == hebrew_message:
            raise MultipleDevicesConnectionException()

    @staticmethod
    def __choose_random_seat(available_seats: list[int]) -> int:
        """
        Selects a random seat number from the given list of available seats.
        :param available_seats: list[int]: The list of available seat numbers.
        :return: int: A randomly selected seat number.
        """
        return random.choice(available_seats)
