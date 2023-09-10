"""
Author: raviv steinberg
Date: 04/09/2023
"""
import argparse


class ArgumentParser:
    """
    Command-line argument parser for the Holmes Place lessons registration utility.
    """

    def __init__(self):
        """
        Initializes the ArgumentParser class and sets up the command-line arguments.
        """
        self.parser = argparse.ArgumentParser(description='Holmes Place lessons registration utility.')
        self._setup_arguments()

    def _setup_arguments(self) -> None:
        """
        Configures the command-line arguments.
        :returns: None
        Note: This is an internal method and should not be used directly outside the class.
        """
        self.parser.add_argument('-u', '--user', type=str, required=True, help='Holmes place user name.')
        self.parser.add_argument('-p', '--password', type=str, required=True, help='Holmes place password.')
        self.parser.add_argument('-d', '--day', type=int, required=True, help='Day of the week (1 for Sunday, 7 for Saturday).')
        self.parser.add_argument('-c', '--exercise', type=int, required=False, default=3, help='Exercise type.')
        self.parser.add_argument('-s', '--start_time', type=str, required=True, help='Start time.')
        self.parser.add_argument('-b', '--seats', nargs='+', type=str, required=True, help='First N priority seats.')
        self.parser.add_argument('-t', '--timeout', type=int, required=True, help='Timeout in seconds.')

    @property
    def parse(self) -> argparse.Namespace:
        """
        Parses the command-line arguments and returns the parsed object.
        :return: argparse.Namespace: The parsed command-line arguments.
        """
        return self.parser.parse_args()
