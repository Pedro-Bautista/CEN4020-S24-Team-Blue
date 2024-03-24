from incollege.entity.Chats import Chats
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper(Chats, 'chats', ['chat_id', 'user1', 'user2'])

def create_chat(obj: Chats):
    UNIVERSAL.create_object(obj)

def delete_chat(obj: Chats):
    UNIVERSAL.delete_object(obj)
    
def get_chats_by_user(user1: str):
   list1 = UNIVERSAL.get_objects_intersection({'user1': user1})
   list2 = UNIVERSAL.get_objects_intersection({'user2': user1})
   
   results = list1 + list2
   
   if results:
       return results

def get_chat(chat_id: str):
    result = UNIVERSAL.get_objects_intersection({'chat_id': chat_id})
    if result:
        return result[0]
    
def get_chat_by_both_users(user1: str, user2: str):
    result = UNIVERSAL.get_objects_intersection({'user1': user1, 'user2': user2})
    if result:
        return result[0]
    return None