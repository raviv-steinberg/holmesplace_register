"""
Author: raviv steinberg
Date: 04/09/2023
"""
import json
from src.api.request_handler import RequestHandler
from typing import Any, Optional, Union, Dict, List
from http import HTTPStatus
import requests
from src.exceptions.bike_occupied_exception import BikeOccupiedException
from src.exceptions.lesson_not_open_for_registration import LessonNotOpenForRegistrationException
from src.exceptions.lesson_time_does_not_exist import LessonTimeDoesNotExistException
from src.exceptions.no_matching_subscription import NoMatchingSubscriptionException
from src.exceptions.registration_for_this_lesson_already_exists import RegistrationForThisLessonAlreadyExistsException
from src.utils.logger_manager import LoggerManager


class ApiHandler:
    """
    Utility class to make HTTP requests and handle their responses.
    This class encapsulates methods to interact with APIs and retrieve data from remote servers using various HTTP
    methods like 'GET', 'POST', 'PUT', and 'DELETE'. It internally uses the popular Python library 'requests' to handle
    the HTTP requests and responses.

    Example Usage:
        # Make a GET request to a URL and parse the JSON response.\n
        response_data = ApiHandler.request('GET', some_url)\n
        # This will print the parsed JSON response:\n
        print(response_data) \n

        # Make a POST request with some data\n
        response_data = ApiHandler.request('POST', some_url json={'name': 'John Doe', 'email': 'john@example.com'})\n
        # This will print the parsed JSON response\n
        print(response_data)\n
    """

    NO_MATCHING_SUBSCRIPTION_FOUND_ERROR_CODE = '26'
    LESSON_TIME_DOES_NOT_EXIST_ERROR_CODE = '30'
    REGISTRATION_FOR_THIS_LESSON_ALREADY_EXISTS_ERROR_CODE = '32'
    BIKE_TAKEN_ERROR_CODE = '33'
    LESSON_IS_NOT_OPEN_FOR_REGISTRATION_ERROR_CODE = '50'

    @staticmethod
    def request(method: str, url: str, *args: Any, **kwargs: Any) -> Any:
        """
        Make an HTTP request using the specified method.
        :param method: str: The HTTP method for the request, e.g., 'GET', 'POST', 'PUT', 'DELETE', etc.
        :param url: str: The URL to make the request to.
        :param args: Any: (optional) Any additional positional arguments to pass to the 'requests' library.
        :param kwargs: Any: (optional) Any additional keyword arguments to pass to the 'requests' library.
        :return: Any: The parsed JSON response from the server (if available).
        """
        ApiHandler.__log_request(method=method, url=url, args=args, kwargs=kwargs)
        response = ApiHandler.__handle_response(response=RequestHandler.make_request(method, url=url, **kwargs))
        ApiHandler.__log_response(url=url, response=response)
        return response

    @staticmethod
    def __handle_response(response: requests.Response) -> Any:
        """
        Processes and handles the given HTTP response from the API. This method specifically checks for certain
        error codes within the response and raises corresponding exceptions based on the error encountered.
        The method expects the response content to be in JSON format, containing potential keys like 'success' and 'error'.
        :param response: The response object returned after making an HTTP request.
        :returns: The parsed JSON data from the response, if successful.
        :raises NoMatchingSubscriptionException: If the error in the response matches the
        "No Matching Subscription Found" error code.
        :raises LessonTimeDoesNotExistException: If the error in the response matches the
        "Lesson Time Does Not Exist" error code.
        :raises RegistrationForThisLessonAlreadyExistsException: If the error in the response matches the
        "Registration For This Lesson Already Exists" error code.
        :raises BikeOccupiedException: If the error in the response matches the "Bike Taken" error code.
        :raises LessonNotOpenForRegistrationException: If the error in the response matches the
        "Lesson Is Not Open For Registration" error code.
        :raises Exception: For any other unexpected errors.
        """
        # Convert response content to a JSON dictionary.
        data = ApiHandler.__parse_json_response(response=response)
        if data:
            # Use .get() to avoid KeyError
            success = data.get('success', False)
            error = data.get('error')

            if not success and error:
                error = data['error']
                if ApiHandler.NO_MATCHING_SUBSCRIPTION_FOUND_ERROR_CODE in error:
                    raise NoMatchingSubscriptionException()
                elif ApiHandler.LESSON_TIME_DOES_NOT_EXIST_ERROR_CODE in error:
                    raise LessonTimeDoesNotExistException()
                elif ApiHandler.REGISTRATION_FOR_THIS_LESSON_ALREADY_EXISTS_ERROR_CODE in error:
                    raise RegistrationForThisLessonAlreadyExistsException()
                elif ApiHandler.BIKE_TAKEN_ERROR_CODE in error:
                    raise BikeOccupiedException(error)
                elif ApiHandler.LESSON_IS_NOT_OPEN_FOR_REGISTRATION_ERROR_CODE in error:
                    raise LessonNotOpenForRegistrationException()
                else:
                    raise Exception(error)

        try:
            # This will raise an HTTPError if the HTTP response status code indicates an error.
            response.raise_for_status()
            if response.status_code == HTTPStatus.OK:
                return response
        except requests.exceptions.HTTPError as http_err:
            raise requests.exceptions.HTTPError(f'HTTP error occurred: {http_err}')
        except requests.exceptions.RequestException as req_err:
            raise requests.exceptions.RequestException(f'Request error occurred: {req_err}')

    @staticmethod
    def __parse_json_response(response: requests.Response) -> Optional[Union[Dict[str, Any], List[Any], str, int, float, bool]]:
        """
        Attempts to parse a response's content as JSON.
        :param response: The response object to parse.
        :return: The parsed JSON object if successful, otherwise None.
        """
        try:
            return response.json()
        except json.JSONDecodeError:
            return None

    @staticmethod
    def __log_request(method: str, url: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs the details of an HTTP request.
        :param method: HTTP method of the request (e.g., GET, POST).
        :param url: The full URL endpoint for the request.
        :param args: Any additional positional arguments (not used in this method, but kept for flexibility).
        :param kwargs: Additional keyword arguments, typically parameters sent with the request.
        :returns: None.
        """
        logger = LoggerManager().logger
        log_data = {'Request Method': method, 'Request URL': url, 'Additional Params': kwargs}
        log_data = {k: v for k, v in log_data.items() if v}
        for key, value in log_data.items():
            logger.debug(msg=f'{key}: {value}')

    @staticmethod
    def __log_response(url: str, response: requests.Response) -> None:
        """
        Logs the details of an HTTP response.
        :param url: The full URL endpoint that the response is associated with.
        :param response: The response object returned after making an HTTP request.
        :returns: None.
        """
        logger = LoggerManager().logger
        content = response.text
        if '?action=logout' in url:
            content = "Response for logout. Full content omitted for brevity."
        log_data = {"Response Status": response.status_code, "Response Headers": dict(response.headers), "Response Content": content}
        log_data = {k: v for k, v in log_data.items() if v}
        for key, value in log_data.items():
            logger.debug(msg=f'{key}: {value}')
