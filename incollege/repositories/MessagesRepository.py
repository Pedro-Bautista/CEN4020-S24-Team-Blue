from incollege.entity.Messages import Messages
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper(Messages, 'messages', ['chat_id', 'message_id'])

def create_message(obj: Messages):
    UNIVERSAL.create_object(obj)
    
def delete_message(obj: Messages):
    UNIVERSAL.delete_object(obj)
    
def get_messages_by_chat_id(chat_id : str):
    UNIVERSAL.get_objects_intersection({'chat_id' : chat_id})
