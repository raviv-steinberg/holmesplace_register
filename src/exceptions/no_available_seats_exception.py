class NoAvailableSeatsException(Exception):
    def __init__(self):
        super().__init__('There are no available seats for this lesson')
