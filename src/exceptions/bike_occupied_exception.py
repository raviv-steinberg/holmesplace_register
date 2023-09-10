class BikeOccupiedException(Exception):
    def __init__(self, arg):
        self.errors = arg
        super().__init__(f'seat {arg} is occupied by another club member')
