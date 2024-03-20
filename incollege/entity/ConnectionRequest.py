from incollege.entity.enum.ConnectionRequestStatus import ConnectionRequestStatus


class ConnectionRequest:
    """This object stores data relating to user connection requests.

    Attributes:
        sender_user_id (str): Unique identifier for sending :obj:`User`.
        recipient_user_id (str): Unique identifier for receiving :obj:`User`.
        status (int): Current status of request as specified by :class:`~ConnectionRequestStatus`.
    """

    def __init__(self, sender_user_id: str, recipient_user_id: str, status: int = ConnectionRequestStatus.PENDING):
        """Generate an instance based on the specified parameters.

        Args:
            sender_user_id (str): Unique identifier for sending :obj:`User`.
            recipient_user_id (str): Unique identifier for receiving :obj:`User`.
            status (int, optional): Current status of request as specified by :class:`~ConnectionRequestStatus`.
                Defaults to ConnectionRequestStatus.PENDING.
        """
        self.sender_user_id = sender_user_id
        self.recipient_user_id = recipient_user_id
        self.status = status
