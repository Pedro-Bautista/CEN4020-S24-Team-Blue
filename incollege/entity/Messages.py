from incollege.entity.enum.MessagesStatus import MessageStatus
from datetime import datetime

class Messages:

    def __init__(self, chat_id: str, message_id: str, sender_id: str, content: str, timestamp = datetime.now(), status: int = MessageStatus.UNREAD):

        self.chat_id = chat_id
        self.message_id = message_id
        self.sender_id = sender_id
        self.content = content
        self.timestamp = timestamp
        self.status = status
        