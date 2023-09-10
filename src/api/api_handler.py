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
        return ApiHandler.__handle_response(response=RequestHandler.make_request(method, url=url, **kwargs))

    @staticmethod
    def __handle_response(response: requests.Response) -> Any:
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
