"""
Author: raviv steinberg
Date: 04/09/2023
"""
from pathlib import Path


class Project:
    """
    The ProjectDirectory class provides a static method for retrieving the root path of the project directory.
    It uses Python's pathlib module to handle file and path operations, making it cross-platform compatible and easy to work with paths.
    """

    @staticmethod
    def root_path() -> Path:
        """
        This method returns the root path of the project directory.
        :return: A Path object representing the root path of the project.
        """
        return Path(__file__).parent.parent.parent
