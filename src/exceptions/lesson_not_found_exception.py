class LessonNotFoundException(Exception):
    def __init__(self, lesson_type: str = None, club_id: int = None, day_of_week: str = None, time: str = None, lesson_id: str = None):
        if lesson_id:
            super().__init__(f'No lesson with ID \'{lesson_id}\' found.')
        else:
            super().__init__(f'No lesson of type \'{lesson_type}\' found in club {club_id} on \'{day_of_week}\' at \'{time}\'.')
