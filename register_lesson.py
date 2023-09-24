"""
Author: raviv steinberg
Date: 09/09/2023
"""
import argparse
from src.services.smtp_service import SMTPService
from src.services.user_data_service import UserDataService
from src.utils.date_utils import DateUtils
from src.utils.lesson_registration_manager_factory import LessonRegistrationManagerFactory

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "This script attempts to register a user for a lesson based on the provided lesson ID.\n"
            "The details of the user and other configurations are fetched from a YAML data file.\n"
            "If the registration fails, the reason is logged for further diagnosis.\n"
            "The script leverages the `LessonRegistrationManagerFactory` to manage the registration process."
        ),
        epilog=(
            "Example:\n"
            "   $ python register_lesson.py -f /path/to/user_data.yaml -l 12345\n\n"
            "Requirements:\n"
            "   - You need to have the required modules installed and available in the script's environment.\n\n"
            "Author: [Your Name]\n"
            "Date: [Current Date]"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--lesson-id', '-l', type=str, required=True, help='Lesson id that the user wats to register to')
    parser.add_argument('--user_data_file', '-f', type=str, required=True, help='User YAML data file')
    args = parser.parse_args()

    lesson_registration_manager = LessonRegistrationManagerFactory(user_data_service=UserDataService(filepath=args.user_data_file), lesson_id=args.lesson_id).get()
    # email = SMTPService()
    # message = f'<p>Lesson: <strong>{lesson_registration_manager.lesson["type"]}</strong></p>' \
    #           f'<p>Day: <strong>{lesson_registration_manager.lesson["day"]}</strong></p>' \
    #           f'<p>Time: <strong>{DateUtils.convert_time_format(time_str=lesson_registration_manager.lesson["start_time"])} on {lesson_registration_manager.lesson["date"]}</strong></p>' \
    #           f'<p>Seat(s): <strong>{", ".join(map(str, lesson_registration_manager.seats))}</strong></p>'
    #
    # email.send(subject='Registration starting', message=message, recipient='raviv.steinberg@gmail.com')
    lesson_registration_manager.register_lesson()
