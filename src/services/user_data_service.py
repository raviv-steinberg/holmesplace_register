"""
Author: raviv steinberg
Date: 14/09/2023
"""
from src.utils.yaml_handler import YAMLHandler


class UserDataService:
    """
    UserDataService is a service class responsible for managing and manipulating user data
    from a YAML file. It offers features to get and set club_id, user credentials (username
    and password), user choices/schedules, and provides utilities for handling lesson
    registration statuses.
    """

    def __init__(self, filepath: str):
        """
        Initializes the UserDataService with the specified filepath.
        Reads the user data YAML file and sets the club_id, user, password, and choices properties.
        :param filepath: Path to the user data YAML file.
        """
        self.filepath = filepath
        content = YAMLHandler.get_content(self.filepath)
        self._club_id = content.get('club_id')
        self._user = content.get('credentials')['user']
        self._password = content.get('credentials')['password']
        self._name = content.get('name')
        self._email = content.get('email')
        self._choices = content.get('user_schedule', [])
        self._notify = content.get('notify', None)

    @property
    def club_id(self) -> int:
        """
        Gets the club_id from the user data.
        :return: An integer representing the club_id.
        """
        return self._club_id

    @club_id.setter
    def club_id(self, value: int):
        """
        Sets the club_id in the user data.
        :param value: An integer representing the club_id.
        """
        self._club_id = value
        self._update_user_data('club_id', value)

    @property
    def user(self) -> str:
        """
        Gets the user from the user data.
        :return: A string representing the user.
        """
        return self._user

    @property
    def password(self) -> str:
        """
        Gets the password from the user data.
        :return: A string representing the password.
        """
        return self._password

    @property
    def name(self) -> str:
        """
        Gets the name from the user data.
        :return: A string representing the name.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """
        Sets the name in the user data.
        :param value: A string representing the name.
        """
        self._name = value
        self._update_user_data('name', value)

    @property
    def email(self) -> str:
        """
        Gets the password from the user data.
        :return: A string representing the password.
        """
        return self._email

    @email.setter
    def email(self, value: str):
        """
        Sets the password in the user data.
        :param value: A string representing the password.
        """
        self._email = value
        self._update_user_data('email', value)

    @property
    def choices(self) -> list:
        """
        Gets the choices (user_schedule) from the user data.
        :return: A list of dictionaries representing the user's choices.
        """
        return self._choices

    @property
    def notify(self) -> bool:
        """
        Gets the Notify value from the user data.
        :return: A boolean value indicate if the user wants to be Notify by email about the registration results..
        """
        return True if self._notify else False

    @choices.setter
    def choices(self, value: list):
        """
        Sets the choices (user_schedule) in the user data.
        :param value: A list of dictionaries representing the user's choices.
        """
        self._choices = value
        self._update_user_data('user_schedule', value)

    def _update_user_data(self, key: str, value):
        """
        Updates the specified key in the user data YAML file with the provided value.
        :param key: A string representing the key to be updated.
        :param value: The new value for the specified key.
        """
        content = YAMLHandler.get_content(self.filepath)
        content[key] = value
        YAMLHandler.write_content(self.filepath, content)

    def get_registration_status(self, lesson_id: str) -> str:
        """
        Retrieves the registration status of a given lesson from the user data file.
        :param lesson_id: ID of the lesson whose registration status needs to be fetched.
        :return: A string representing the registration status.
        """
        content = YAMLHandler.get_content(self.filepath)
        for lesson in content.get('user_schedule', []):
            if lesson['lesson_id'] == lesson_id:
                return lesson.get('registration_status', 'idle')
        # Default to 'idle' if lesson_id is not found.
        return 'idle'

    def is_registration_in_progress(self, lesson_id: str) -> bool:
        """
        Checks if the registration for a given lesson is in progress.
        :param lesson_id: ID of the lesson to check.
        :return: True if registration is in progress, False otherwise.
        """
        for lesson in self._choices:
            if lesson['lesson_id'] == lesson_id:
                return lesson.get('in_progress', False)
        # Default to False if lesson_id is not found.
        return False

    def set_registration_progress(self, lesson_id: str, in_progress: bool):
        """
        Sets the registration progress status of a given lesson.
        :param lesson_id: ID of the lesson whose registration progress needs to be set.
        :param in_progress: A boolean indicating if the registration is in progress.
        """
        for lesson in self._choices:
            if lesson['lesson_id'] == lesson_id:
                lesson['in_progress'] = in_progress
                break
        self._update_user_data('user_schedule', self._choices)
