import uuid
from typing import List

from incollege.entity.enum.ConnectionRequestStatus import ConnectionRequestStatus, from_string
from incollege.exceptions.ContentException import ContentException
from incollege.repositories import ConnectionRepository, UserRepository, ChatsRepository
from incollege.entity.Chats import Chats

def create_chat_id():
    return str(uuid.uuid4())

def create_chat(user1, user2):
    if not user1 or not user2:
        raise ContentException('Required parameters not provided.', 400)
    if not UserRepository.get_user(user1):
        raise ContentException('No such sending user.', 404)
    if not UserRepository.get_user(user2):
        raise ContentException('No such sending user.', 404)
    if ChatsRepository.get_chat_by_both_users(user1, user2):
        raise ContentException('Chat between users already exists', 409)
    if ChatsRepository.get_chat_by_both_users(user2, user1):
        raise ContentException('Chat between users already exists', 409)
    user = UserRepository.get_user(user1)
    user_tier = user.tier 
    if user_tier == 'standard':
        if not ConnectionRepository.connection_check(user1, user2) and not ConnectionRepository.connection_check(user2, user1):
            raise ContentException('Cannot create chat if not connected', 404)
    
    chat_id = create_chat_id()
    chat = Chats(chat_id, user1, user2)

    ChatsRepository.create_chat(chat)
    

def get_chat_list(user1):
    result = ChatsRepository.get_chats_by_user(user1)
    if not result:
        raise ContentException('No matching chats found', 404)
    return result
    
def get_chat(chat_id: str):
    if not chat_id:
        raise ContentException('Required chat identifier information not provided.', 400)
    chat = ChatsRepository.get_chat(chat_id)
    if not chat:
        raise ContentException('No such chat.', 404)
    
    return chat