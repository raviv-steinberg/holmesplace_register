class LessonCanceledException(Exception):
    def __init__(self):
        super().__init__('The lesson was canceled')