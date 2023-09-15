"""
Author: raviv steinberg
Date: 09/09/2023
"""
import time

from src.services.user_data_service import UserDataService
from src.utils.lessons_manager import LessonsManager
import json
import subprocess
import argparse

NOTIFY_REGISTRATION_SCRIPT = 'notify_registration.py'
REGISTER_LESSON_SCRIPT = 'register_lesson.py'


def fetch_notifier_tuple(file: str):
    return_code, output = subprocess.getstatusoutput(cmd=f'python {NOTIFY_REGISTRATION_SCRIPT} -f {file} -t {args.threshold}')
    return tuple(json.loads(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "This script notifies the user when a lesson registration time is nearing based on the specified threshold value.\n"
            "If the threshold is reached, it attempts to register the user for the lesson using provided user data.\n\n"
            "The script uses two sub-scripts for this process:\n"
            "   1. NOTIFY_REGISTRATION_SCRIPT: Checks if lesson registration is nearing based on threshold.\n"
            "   2. REGISTER_LESSON_SCRIPT: Registers the user to the lesson if the threshold is met.\n"
        ),
        epilog=(
            "Example:\n"
            "   $ python main_script.py -f /path/to/user_data.yaml -t 3\n\n"
            "Requirements:\n"
            "   - You need to have the required modules installed and available in the script's environment.\n\n"
            "Author: [Your Name]\n"
            "Date: [Current Date]"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--user_data_file', '-f', type=str, required=True, help='User YAML data file')
    parser.add_argument('--threshold', '-t', type=float, required=True, help='Threshold value in minutes')
    args = parser.parse_args()

    user_data_service = UserDataService(filepath=args.user_data_file)
    user_file = f'"{args.user_data_file}"'
    lesson_id, minutes = fetch_notifier_tuple(file=user_file)

    if lesson_id and minutes:
        is_in_progress = user_data_service.is_registration_in_progress(lesson_id=lesson_id)
        if not is_in_progress:
            details = LessonsManager().retrieve_lesson_details(lesson_id=lesson_id)
            subprocess.Popen(['python', REGISTER_LESSON_SCRIPT, '-f', args.user_data_file, '-l', lesson_id])
