"""
Author: raviv steinberg
Date: 04/09/2023
"""
from typing import Any
import requests


class RequestHandler:
    """
    The RequestHandler class is designed to handle and store a session object to facilitate
    making HTTP requests using the requests library in a Python project.
    It provides two class methods, get_session() and make_request(),
    to manage the session and make HTTP requests, respectively.
    """
    session = None

    @classmethod
    def get_session(cls) -> requests.Session:
        """
        Get or create a shared requests Session for making HTTP requests.
        :return: requests.Session: A shared session object.
        """
        if cls.session is None:
            cls.session = requests.Session()
        return cls.session

    @classmethod
    def make_request(cls, method: str, **kwargs: Any) -> requests.Response:
        """
        Make an HTTP request using the specified method and keyword arguments.
        :param method: method: The HTTP method for the request, e.g., 'GET', 'POST', 'PUT', 'DELETE', etc.
         or if any other requests.exceptions.RequestException occurs while making the request.
        :raises requests.exceptions.Timeout: If the request times out after the specified timeout period.
        :raises requests.exceptions.RequestException: If the 'url' keyword argument is not provided. or if there are invalid keyword arguments provided,
         which are not allowed by the Requests library
        """
        url = kwargs.get('url', None)
        if not url:
            raise ValueError('URL is required.')

        allowed_args = set(requests.Request.__init__.__code__.co_varnames)
        invalid_args = set(kwargs.keys()) - allowed_args
        if invalid_args:
            raise ValueError(f'Invalid keyword arguments: {{'',''.join(invalid_args)}}')
        session = cls.get_session()

        # Customizable timeout support with a default timeout of 10 seconds.
        timeout = kwargs.get('timeout', 60)

        try:
            return session.request(method, timeout=timeout, **kwargs)
        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout(f'Request timed out after {timeout} seconds.')
        except requests.exceptions.RequestException as ex:
            raise requests.exceptions.RequestException(f"Request failed: {ex}")
