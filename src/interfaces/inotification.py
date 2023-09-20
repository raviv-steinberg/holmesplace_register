from abc import ABC, abstractmethod


class INotification(ABC):
    """
    Defines the contract for sending notifications.
    This interface is intended to standardize the methods and expectations for
    sending notifications, whether they be email, SMS, or any other type.
    Derived classes should provide concrete implementations for specific
    notification methods.
    """

    @abstractmethod
    def send(self, recipient: str, subject:str, message: str) -> None:
        """
        Sends a notification to the specified recipient.
        :param recipient: The target recipient of the notification.
        :param subject: The subject of the notification.
        :param message: The content or body of the notification.
        :return: None
        :raises NotImplementedError: This method should be implemented by the derived class.
        """
        raise NotImplementedError
