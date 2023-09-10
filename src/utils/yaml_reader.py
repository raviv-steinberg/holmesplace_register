"""
Author: raviv steinberg
Date: 08/09/2023
"""
import yaml


class YAMLReader:
    @staticmethod
    def get_content(filepath: str) -> dict:
        """
        Reads the YAML file content and returns it as a dictionary.
        :param filepath: str: Path to the YAML file to be read.
        :return: dict: Content of the YAML file.
        """
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)
