from enum import Enum


class DaysOfWeek(Enum):
    """
    Represents the days of the week in Hebrew.
    Each member of this enum corresponds to a day of the week in Hebrew.
    """
    SUNDAY = "ראשון"
    MONDAY = "שני"
    TUESDAY = "שלישי"
    WEDNESDAY = "רביעי"
    THURSDAY = "חמישי"
    FRIDAY = "שישי"
    SATURDAY = "שבת"

    @staticmethod
    def get_hebrew_day(english_day: str) -> str:
        """
        Get the Hebrew representation of a day based on its English representation.
        :param english_day: The English representation of the day.
        :return: The Hebrew representation of the day.
        :raises ValueError: If the English day string is not found.
        """
        for day in DaysOfWeek:
            if day.name == english_day:
                return day.value
        raise ValueError(f"No Hebrew representation found for day '{english_day}'")
