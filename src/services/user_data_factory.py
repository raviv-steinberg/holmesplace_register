"""
Author: raviv steinberg
Date: 03/05/2024
"""
import os.path

from src.services.user_data_service import UserDataService


class UserDataFactory:
    """
    Returns a UserDataService object for the specified username.
    """
    users_data_dir = 'users_data'

    @staticmethod
    def get_user_data_service(username: str) -> UserDataService:
        """
        Returns a UserDataService object for the specified username.
        :param username: Name of the user for whom data needs to be fetched.
        :return: UserDataService object.
        :raise FileNotFoundError: If the user data file for the specified username does not exist.
        """
        filepath = os.path.join(UserDataFactory.users_data_dir, f'{username}.yaml')
        if os.path.exists(filepath):
            return UserDataService(filepath)
        raise FileNotFoundError(f'User data file not found for user \'{username}\'')
