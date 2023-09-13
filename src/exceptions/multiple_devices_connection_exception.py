class MultipleDevicesConnectionException(Exception):
    def __init__(self):
        super().__init__('Cannot log in with the same account from multiple devices')
