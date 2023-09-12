class UserPreferredSeatsOccupiedException(Exception):
    def __init__(self, message: str = 'All user-preferred seats are occupied'):
        super().__init__(message)