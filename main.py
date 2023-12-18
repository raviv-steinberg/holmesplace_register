import time
from src.services.user_data_service import UserDataService
from src.services.user_lesson_scheduler_service import UserLessonSchedulerService
from src.utils.date_utils import DateUtils
from src.utils.lesson_registration_manager_factory import LessonRegistrationManagerFactory

if __name__ == "__main__":
    # Exception: (36) השיעור מלא.
    threshold = 1000000
    sleep_time = 60
    source_user_data_file = 'users_data/raviv.yaml'
    service = UserDataService(filepath=source_user_data_file)
    user_lesson_scheduler_service = UserLessonSchedulerService(user_data_service=service)
    lesson_id, minutes = user_lesson_scheduler_service.monitor_registration_time(threshold_minutes=threshold)
    if lesson_id:
        manager = LessonRegistrationManagerFactory(user_data_service=service, lesson_id=lesson_id).get()
        manager.register_lesson()
    # else:
    #     print(f'[{DateUtils.current_time()}]: No lesson found that starts within {threshold} minutes, sleep {sleep_time} seconds and retry...')
    #     time.sleep(sleep_time)
