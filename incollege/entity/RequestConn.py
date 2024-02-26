class connectionRequest:
    def __init__(self, request_id, sender_user_id, receiver_user_id, status='pending'):
        self.request_id = request_id
        self.sender_user_id = sender_user_id
        self.receiver_user_id = receiver_user_id
        self.status = status
