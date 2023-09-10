"""
Author: raviv steinberg
Date: 06/09/2023
"""


class SingletonMeta(type):
    """
    Singleton Metaclass.
    Ensures that a single instance of a class is created and shared among all other instances.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Overloads the call method to return the single instance.
        :param args: tuple: Arguments for the class instantiation.
        :param kwargs: dict: Keyword arguments for the class instantiation.
        :return: object: The single instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
