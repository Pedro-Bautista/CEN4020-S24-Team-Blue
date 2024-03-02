from incollege.entity.enum.ConnectionRequestStatus import ConnectionRequestStatus


class ConnectionRequest:

    def __init__(self, sender_user_id, recipient_user_id, status=ConnectionRequestStatus.PENDING):
        self.sender_user_id = sender_user_id
        self.recipient_user_id = recipient_user_id
        self.status = status
