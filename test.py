import time

from src.services.user_lesson_scheduler_service import UserLessonSchedulerService
from src.utils.lesson_registration_manager_factory import LessonRegistrationManagerFactory

# user = '0547713437'
# password = '12345678'
# user = '0547558333'
# password = '12345678'
# user = '0527206014'
# password = 'dana1234'
# user = '0506291251'
# password = 'yaron1357'

source_user_data_file = 'users_data/raviv_user_schedule.yaml'

user_lesson_scheduler_service = UserLessonSchedulerService(source_user_data_file=source_user_data_file)

lesson_id, minutes = user_lesson_scheduler_service.monitor_registration_time(threshold_minutes=30000)
if lesson_id:
    lesson_registration_manager = LessonRegistrationManagerFactory(source_user_data_file=source_user_data_file, lesson_id=lesson_id).get()
    lesson_registration_manager.register_lesson()
