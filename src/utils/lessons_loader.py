"""
Author: raviv steinberg
Date: 06/09/2023
"""
import os
from src.utils.project import Project
from src.utils.singleton_meta import SingletonMeta
from src.utils.yaml_handler import YAMLHandler


class LessonsLoader(metaclass=SingletonMeta):
    """
    Singleton class for loading and providing access to the lessons data from the YAML file.
    Ensures that the file is loaded only once across the application.
    """
    FILE_NAME = 'holmes_lessons.yaml'

    def __init__(self, lessons_file_path=None):
        """
        Initializes the LessonsLoader class.

        :param lessons_file_path: str, optional: Path to the YAML file containing lessons information.
                                  Default is 'holmes_lessons.yaml' in the current working directory.
        """
        if lessons_file_path is None:
            lessons_file_path = os.path.join(Project.root_path(), self.FILE_NAME)
        self.lessons_file_path = lessons_file_path
        self.lessons = self._load_lessons()

    def _load_lessons(self) -> dict:
        """
        Loads the lessons from the specified YAML file.

        :return: dict: A dictionary containing lessons data.
        Note: This is a private method and should not be used directly outside the class.
        """
        return YAMLHandler.get_content(filepath=self.lessons_file_path)
