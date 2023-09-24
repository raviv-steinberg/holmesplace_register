from abc import ABC, abstractmethod
from typing import Any


class IGoogleService(ABC):
    """
    Abstract base class for Google services.
    """

    @abstractmethod
    def authenticate(self) -> Any:
        """
        Authenticates the user and returns the service for a specific Google API.
        :return: An authenticated service for Google Calendar API.
        """
        raise NotImplementedError

    @abstractmethod
    def get_scopes(self) -> list:
        """
        Returns the list of scopes required for the Google service.
        """
        raise NotImplementedError
