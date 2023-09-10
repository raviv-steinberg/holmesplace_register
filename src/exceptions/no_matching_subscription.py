class NoMatchingSubscriptionException(Exception):
    def __init__(self):
        super().__init__('No matching subscription found')
