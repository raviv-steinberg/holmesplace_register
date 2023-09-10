class LessonTimeDoesNotExistException(Exception):
    def __init__(self):
        super().__init__('Lesson time does not exist')
