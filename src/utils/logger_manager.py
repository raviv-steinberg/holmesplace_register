"""
Author: raviv steinberg
Date: 05/09/2023
"""
from src.utils.singleton_meta import SingletonMeta
import logging
import os
from datetime import datetime
from logging.config import dictConfig
import coloredlogs


class LoggerManager(metaclass=SingletonMeta):

    def __init__(self, user=None):
        # Return early if the instance already exists
        # This ensures __init__ logic is only executed once
        if getattr(self, "_initialized", False):
            return

        self.user = user
        if self.user is None:
            raise ValueError("User must be specified for LoggerManager")
        filename = self.__create_directory_structure()

        config = {
            'version': 1,
            'loggers': {
                'crumbs': {
                    'level': 'DEBUG',
                    'handlers': ['file_handler', 'stdout_handler'],
                },
            },
            'handlers': {
                'file_handler': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': filename,
                    'backupCount': 3,
                    'formatter': 'simple',
                },
                "stdout_handler": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    'formatter': 'simple',
                }
            },
            'formatters': {
                'simple': {
                    'format': '[%(asctime)s] [ %(levelname)s ] [%(filename)s] [%(funcName)s] [%(lineno)d]: %(message)s',
                },
            },
        }

        dictConfig(config)
        coloredlogs.install(logger=self.logger, level='DEBUG')
        self._initialized = True

    def __create_directory_structure(self) -> str:
        """
        Creates a directory structure as Year/Month/Date and returns the full path for the log file.
        :return: The full path for the log file.
        """
        now = datetime.now()
        year_directory = f'./logs/{now.year}'
        month_directory = f'{year_directory}/{now.strftime("%B")}'
        date_directory = f'{month_directory}/{now.strftime("%d-%m-%Y")}'

        # Create directories as needed.
        os.makedirs(date_directory, exist_ok=True)

        # Create the filename.
        return f'{date_directory}/{self.user}-{str(now.hour).zfill(2)}-{str(now.minute).zfill(2)}.log'

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger('crumbs')
