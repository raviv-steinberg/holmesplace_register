"""
Author: raviv steinberg
Date: 09/09/2023
"""
from src.utils.lessons_manager import LessonsManager
import json
import subprocess
import argparse

NOTIFY_REGISTRATION_SCRIPT = 'notify_registration.py'
REGISTER_LESSON_SCRIPT = 'register_lesson.py'


def fetch_notifier_tuple():
    return tuple(json.loads(subprocess.check_output(f'python3 {NOTIFY_REGISTRATION_SCRIPT} -f {args.user_data_file} -t {args.threshold}', shell=True).decode("utf-8")))


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

    lesson_id, minutes = fetch_notifier_tuple()
    if lesson_id and minutes:
        details = LessonsManager().retrieve_lesson_details(lesson_id=lesson_id)
        subprocess.Popen(['python3', REGISTER_LESSON_SCRIPT, '-f', args.user_data_file, '-l', lesson_id])
