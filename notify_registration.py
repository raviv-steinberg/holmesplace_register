"""
Author: raviv steinberg
Date: 09/09/2023
"""
import json
from src.services.user_lesson_scheduler_service import UserLessonSchedulerService
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "This script notifies if the registration time for a lesson, as indicated in the user's data, \n"
            "is within a given threshold in minutes. If the condition is met, it outputs a tuple of data\n"
            "related to that lesson in JSON format.\n"
            "The script utilizes the `UserLessonSchedulerService` class to perform the monitoring."
        ),
        epilog=(
            "Example:\n"
            "   $ python notifier.py -f /path/to/user_data.yaml -t 10\n\n"
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

    user_lesson_scheduler_service = UserLessonSchedulerService(source_user_data_file=args.user_data_file)
    lesson_tuple = user_lesson_scheduler_service.monitor_registration_time(threshold_minutes=args.threshold)
    sys.stdout.write(json.dumps(lesson_tuple))
    sys.stdout.flush()
    sys.exit(0)
