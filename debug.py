import os

from src.common.holmes_place_api import HolmesPlaceAPI
from src.utils.lesson_registration_manager import LessonRegistrationManager
from src.utils.lessons_loader import LessonsLoader
from src.utils.lessons_manager import LessonsManager
from src.utils.logger_manager import LoggerManager
from src.utils.project import Project

user = '0547713437'
password = '12345678'
# user = '0547558333'
# password = '12345678'
# user = '0527206014'
# password = 'dana1234'
# user = '0506291251'
# password = 'yaron1357'
logger = LoggerManager().logger

lessons_manager = LessonsManager()
lesson = lessons_manager.get_lesson(club_id=205, lesson_type='pilates', day_of_week='thursday', time='9:30')
logger.debug(lesson)

lesson_registration_manager = LessonRegistrationManager(user=user, password=password, lesson=lesson, api=HolmesPlaceAPI(), seats=[3, 4, 5])
try:
    lesson_registration_manager.register_lesson()
except Exception as ex:
    logger.exception(ex)
finally:
    lesson_registration_manager.logout()
