from enum import Enum


class ConnectionStatus:
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2


class ConnectionRequest:

    def __init__(self, sender_user_id, recipient_user_id, status=ConnectionStatus.PENDING):
        self.sender_user_id = sender_user_id
        self.recipient_user_id = recipient_user_id
        self.status = status
