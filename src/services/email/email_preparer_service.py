import os

from src.utils.date_utils import DateUtils
from src.utils.project import Project


class EmailPreparerService:
    """
    Prepares the email content based on the given lesson details.
    """

    def __init__(self):
        """
        Initializes the email preparer with predefined icons and subjects.
        """
        self.icons = {
            'spinning': '🚴',
            'pilates': '🤸‍♀️',
            'yoga': '🧘‍♀️',
            'shape': '💪',
            'health_exercise': '🏃‍♂️',
            'dynamic_design': '🎨',
            'feldenkrais': '🚶‍♂️',
            'bodypump': '🏋️‍♂️'
        }

        self.subjects = {
            'spinning': "Ride Your Way to Fitness! 🚴",
            'pilates': "Pilates Party Alert! 🤸‍♀️ Are You In?",
            'yoga': "Ready to Find Your Zen? 🧘‍♀️",
            'shape': "Shape Up and Show Off! 💪",
            'health_exercise': "Your Health. Your Move. Let's Go! 🏃‍♂️",
            'dynamic_design': "Designs That Move, Inspire, and Excite! 🎨",
            'feldenkrais': "Discover Movement, Discover Yourself with Feldenkrais! 🚶‍♂️",
            'bodypump': "Pump It Up and Get Ripped! 🏋️‍♂️"
        }

    def prepare_email(self, attendee_name: str,lesson: dict, seat: int) -> tuple[str, str]:
        """
        Prepares the email content based on the given lesson details.
        :param attendee_name: The name of the attendee.
        :param lesson: dict: The lesson details (e.g., {'type': 'spinning', 'time': '10:00 AM', 'day': 'Monday'}).
        :param seat: The registered seat.
        :return: tuple: A tuple containing the email subject and the corresponding HTML content.
        """
        lesson_type = lesson.get('type')
        calender_image_url = 'https://images.emojiterra.com/twitter/v14.0/256px/1f4c5.png'

        if lesson_type not in self.icons:
            raise ValueError(f'Unsupported lesson type: {lesson_type}')

        icon = self.icons[lesson_type]
        subject = self.subjects[lesson_type]
        html_content = f"""        
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                    }}
                    a {{
                        color: #007BFF;
                        text-decoration: none;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                    .aligned-icon {{
                        font-size: 26px; 
                        margin-right: 10px;
                        vertical-align: middle;  /* This will align the icon with the adjacent text */
                    }}
                    .aligned-icon-big {{
                        font-size: 35px; 
                        margin-right: 10px;
                        vertical-align: middle;  /* This will align the icon with the adjacent text */
                    }}
                    .underline-text {{
                        border-bottom: 1px; /* You can adjust the color and thickness as needed */
                        padding-bottom: 3px; /* This gives a little space between the text and the line */
                        display: inline-block; /* This is necessary for padding to affect inline elements */
                        vertical-align: middle; /* This ensures that the text aligns with the icon */
                    }}
                    .details-container {{
                        border-left: 1px solid #ccc;
                        padding-left: 15px; /* This gives a space between the line and the text */
                        display: inline-block;
                    }}
                    .image-icon {{
                    margin-right: 10px;     /* This adds space after the image */
                    vertical-align: middle; /* This aligns the image vertically with the adjacent text */
                }}
                </style>
            </head>
            <body>
                <p>Hey <strong>{attendee_name.capitalize()}</strong>!</p>
                <p>Guess what? Your spot for our <b>{lesson_type}</b> lesson is all set and ready to go! <span style="font-size: 20px;">{icon}</span>‍♂️💨</p>
                <p>But... can you handle the fun? 😜</p>
                <p><img src="{calender_image_url}" alt="Calendar Icon" width="38" height="38" class="image-icon"/><strong class="underline-text">Lesson Details</strong></p>
                <div class="details-container">
                    Lesson: {lesson.get('type')}<br>
                    Day: {lesson.get('day').capitalize()} on {lesson.get('date')}<br>
                    Time: {DateUtils.convert_time_format(time_str=lesson.get('start_time'))}<br>
                    Seat: <span><b>{seat}</b></span>
                </div>
                <p>Can't wait to see you bring your A-game!</p>
                <p>Spin you later!<br>
            </body>
            </html>
            """
        return subject, html_content

