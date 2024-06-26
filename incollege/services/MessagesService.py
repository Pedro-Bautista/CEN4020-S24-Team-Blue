import uuid
from typing import List

from incollege.entity.Messages import Messages
from incollege.exceptions.ContentException import ContentException
from incollege.repositories import UserRepository, ChatsRepository, MessagesRepository
from incollege.entity.enum.MessagesStatus import MessageStatus, from_string

def create_message_id():
    return str(uuid.uuid4())

def create_message(user1: str, chat_id: str, content: str):
    if not chat_id or not content:
        raise ContentException('Required message information not provided.', 400)
    user = UserRepository.get_user(user1)
    if not user:
        raise ContentException('No such user.', 404)
    chat = ChatsRepository.get_chat(chat_id)
    if not chat:
        raise ContentException('No such chat', 404)
    if len(content) > 1000:
        raise ContentException('Message content must not exceed 1000 characters',404)
    message_id = create_message_id()
    message = Messages(chat_id, message_id, user1, content)
    MessagesRepository.create_message(message)
    
def get_messages(user1: str, chat_id: str):
    if not user1 or not chat_id:
        raise ContentException('Cannot get messages with information provided.', 400)
    user = UserRepository.get_user(user1)
    if not user:
        raise ContentException('Do not have sufficient permissions to send message in this chat', 400)
    chat = ChatsRepository.get_chat(chat_id)
    if not chat:
        raise ContentException('No such chat. Cannot send message', 404)
    messages_in_chat = MessagesRepository.get_messages_by_chat_id(chat_id)
    if not messages_in_chat:
        raise ContentException('No messages in this chat.', 404)
    return messages_in_chat

def delete_message(user1: str, message_id: str):
    if not user1 or not message_id:
        raise ContentException('Cannot delete messages with information provided.', 400)
    user = UserRepository.get_user(user1)
    if not user:
        raise ContentException('Do not have sufficient permissions to delete this message.', 400)
    message = MessagesRepository.get_message(message_id)
    if not message:
        raise ContentException('No such message.', 404)
    MessagesRepository.delete_message(message)
    
def change_read_status(user1, chat_id, message_id, status):
    if not user1 or not chat_id or not message_id or not status:
        raise ContentException('Cannot change status with information provided', 400)
    user = UserRepository.get_user(user1)
    if not user:
        raise ContentException('Do not have sufficient permissions to change read status', 400)
    message = MessagesRepository.get_message(message_id)
    if not message:
        raise ContentException('Message does not exist.', 404)
    message.status = from_string(status)
        
    MessagesRepository.change_read_status(message)
    
def get_unread(user1, chat_id):
    if not user1 or not chat_id:
        raise ContentException('Cannot get unread messages with information provided', 400)
    user = UserRepository.get_user(user1)
    if not user:
        raise ContentException('Do not have sufficient permissions to get messages', 400)   
    chat = ChatsRepository.get_chat(chat_id)
    if not chat:
        raise ContentException('Chat does not exist', 404)
    
    result = MessagesRepository.get_unread(chat_id)
    
    return result