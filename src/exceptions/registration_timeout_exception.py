class RegistrationTimeoutException(Exception):
    def __init__(self, message='Registration has timed out'):
        super().__init__(message)
