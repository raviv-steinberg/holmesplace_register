class MultipleDevicesConnectionException(Exception):
    def __init__(self):
        super().__init__('Cannot connect from multiple devices')
