from src.services.email.email_template_provider import EmailTemplateProvider
from src.utils.date_utils import DateUtils


class EmailPreparerService:
    """
    Prepares the email content based on the given lesson details.
    """

    def __init__(self):
        """
        Initializes the email preparer with predefined icons and subjects.
        """
        self.calender_image_url = 'https://images.emojiterra.com/twitter/v14.0/256px/1f4c5.png'

    def prepare_email(self, attendee_name: str, lesson: dict, seat: int) -> tuple[str, str]:
        email_template = EmailTemplateProvider(lesson_type=lesson.get('type'))
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
                        vertical-align: middle;
                    }}
                    .aligned-icon-big {{
                        font-size: 35px; 
                        margin-right: 10px;
                        vertical-align: middle;
                    }}
                    .underline-text {{
                        border-bottom: 1px solid #ccc;
                        padding-bottom: 3px;
                        display: inline-block;
                        vertical-align: middle;
                    }}
                    .details-container {{
                        border-left: 1px solid #ccc;
                        padding-left: 15px;
                        display: inline-block;
                    }}
                    .image-icon {{
                        margin-right: 10px;
                        vertical-align: middle;
                    }}
                    .lesson-header {{
                        font-size: 28;  /* Adjust as necessary for the desired size */
                        vertical-align: middle;
                    }}
                    .lesson-values {{
                        font-size: 22;  /* Adjust as necessary for the desired size */
                        vertical-align: middle;
                    }}
            </style>
        </head>
        <body>
            <p>Hey <strong>{attendee_name.capitalize()}</strong>!</p>
            {email_template.body}
            <p><img src="{self.calender_image_url}" alt="Calendar Icon" width="38" height="38" class="image-icon"/><strong class="lesson-header">Lesson Details</strong></p>
            <div class="details-container">
                Lesson: <span><b>{lesson.get('type').capitalize()}</b></span><br>
                Day: <span ><b>{lesson.get('day').capitalize()} on {lesson.get('date')}</b></span><br>
                Time: <span><b>{DateUtils.convert_time_format(time_str=lesson.get('start_time'))}</b></span><br>
                Seat: <span><b>{seat}</b></span><br>
            </div>
        </body>
        </html>
        """
        return email_template.subject, html_content
