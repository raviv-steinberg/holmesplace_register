"""
Author: raviv steinberg
Date: 08/09/2023
"""
import yaml


class YAMLHandler:
    @staticmethod
    def get_content(filepath: str) -> dict:
        """
        Reads the YAML file content and returns it as a dictionary.
        :param filepath: str: Path to the YAML file to be read.
        :return: dict: Content of the YAML file.
        """
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def write_content(filepath: str, content: dict):
        """
        Writes the given content to a specified YAML file.
        :param filepath: Path to the YAML file to be written.
        :param content: A dictionary representing the content to be written to the file.
        """
        with open(filepath, 'w') as file:
            yaml.dump(content, file)