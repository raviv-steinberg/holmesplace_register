class LessonNotOpenForRegistrationException(Exception):
    def __init__(self):
        super().__init__('At the moment the lesson is not open for registration')
