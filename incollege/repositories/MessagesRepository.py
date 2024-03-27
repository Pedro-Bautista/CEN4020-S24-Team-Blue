from incollege.entity.Messages import Messages
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper
from incollege.entity.Messages import MessageStatus, Messages

UNIVERSAL = UniversalRepositoryHelper(Messages, 'messages', ['chat_id', 'message_id'])

def create_message(obj: Messages):
    UNIVERSAL.create_object(obj)
    
def delete_message(obj: Messages):
    UNIVERSAL.delete_object(obj)
    
def get_messages_by_chat_id(chat_id : str):
    return UNIVERSAL.get_objects_intersection({'chat_id' : chat_id})

def get_message(message_id : str):
    result = UNIVERSAL.get_objects_intersection({'message_id' : message_id})
    if result:
        return result[0]
    
def change_read_status(obj : Messages):
    UNIVERSAL.insert_update_object(obj)
    
def get_unread(chat_id : str):
    result = UNIVERSAL.get_objects_intersection({'chat_id' : chat_id, 'status' : MessageStatus.UNREAD})
    return result