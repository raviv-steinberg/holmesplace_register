import time

from src.enums.lesson_type import LessonType
from src.services.user_data_service import UserDataService
from src.services.user_lesson_scheduler_service import UserLessonSchedulerService
from src.services.whatsapp.whatsapp_service import WhatsappService
from src.utils.date_utils import DateUtils
from src.utils.lesson_registration_manager_factory import LessonRegistrationManagerFactory

days_of_week = {
    "SUNDAY": "ראשון",
    "MONDAY": "שני",
    "TUESDAY": "שלישי",
    "WEDNESDAY": "רביעי",
    "THURSDAY": "חמישי",
    "FRIDAY": "שישי",
    "SATURDAY": "שבת"
}

if __name__ == "__main__":
    # Exception: (36) השיעור מלא.
    threshold = 37565756756
    sleep_time = 60
    source_user_data_file = 'users_data/dana.yaml'
    service = UserDataService(filepath=source_user_data_file)
    user_lesson_scheduler_service = UserLessonSchedulerService(user_data_service=service)
    lesson_id, minutes = user_lesson_scheduler_service.monitor_registration_time(threshold_minutes=threshold)
    if lesson_id:
        manager = LessonRegistrationManagerFactory(user_data_service=service, lesson_id=lesson_id).get()
        rotated_date_str = "/".join(manager.lesson["date"].split("/")[::-1])
        manager.register_lesson()

    # while True:
    #     lesson_id, minutes = user_lesson_scheduler_service.monitor_registration_time(threshold_minutes=threshold)
    #     if lesson_id:
    #         manager = LessonRegistrationManagerFactory(user_data_service=service, lesson_id=lesson_id).get()
    #         rotated_date_str = "/".join(manager.lesson["date"].split("/")[::-1])
    #         manager.register_lesson()
            # day = days_of_week[manager.lesson['day'].upper()]
            # messages = [
            #     f'הרישום לשיעור {LessonType.get_hebrew_name(english_name=manager.lesson["type"].upper())} בוצע בהצלחה! 🎉',
            #     f'',
            #     f'פרטי השיעור:',
            #     f'------------',
            #     f'יום: {day}',
            #     f'תאריך: {rotated_date_str}',
            #     f'שעה: {DateUtils.convert_time_format(time_str=manager.lesson["start_time"])}',
            #     'מקום מספר: *4*',
            #     'נשמח לראותך בשיעור! 💪']
            #
            # WhatsappService.send_message(
            #     contact_name=manager.user_data_service.whatsapp_group_name,
            #     message='\n'.join(messages))
        # else:
        #     print(
        #         f'[{DateUtils.current_time()}]: No lesson found that starts within {threshold} minutes, sleep {sleep_time} seconds and retry...')
        #     time.sleep(sleep_time)
        # break
