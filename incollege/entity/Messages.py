from incollege.entity.enum.MessagesStatus import MessageStatus

class Messages:

    def __init__(self, chat_id: str, message_id: str, content: str, status: int = MessageStatus.UNREAD):

        self.chat_id = chat_id
        self.message_id = message_id
        self.content = content
        self.status = status