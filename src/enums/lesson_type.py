from enum import Enum
from typing import Any


class LessonType(Enum):
    """
    Represents different types of lessons.
    """
    FELDENKRAIS = "פלדנקרייז"
    FITBALL = "פיטבול"
    YOGA = "יוגה"
    HEALTH_EXERCISE = "התעמלות בריאותית"
    SPINNING = "ספינינג"
    PILATES = "פילאטיס"
    SCULPTING = "עיצוב"
    DYNAMIC_DESIGN = "עיצוב דינאמי"

    @staticmethod
    def get_hebrew_name(english_name: str) -> Any:
        """
        Get the Hebrew name of a lesson type based on its English name.
        :param english_name: The English name of the lesson type.
        :type english_name: str
        :return: The Hebrew name of the lesson type.
        :rtype: str
        """
        for lesson_type in LessonType:
            if lesson_type.name == english_name:
                return lesson_type.value
        raise ValueError(f"No Hebrew name found for lesson type '{english_name}'")
