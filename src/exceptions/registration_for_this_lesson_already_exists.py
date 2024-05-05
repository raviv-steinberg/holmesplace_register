class RegistrationForThisLessonAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__('Registration for this lesson already exists')
