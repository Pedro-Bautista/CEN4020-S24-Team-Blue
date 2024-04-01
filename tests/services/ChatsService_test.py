import pytest
from unittest.mock import MagicMock, patch

from incollege.entity.User import User
from incollege.exceptions import ContentException
from incollege.services.ChatsService import *


@pytest.fixture
def mock_user_repository():
    return MagicMock()


@pytest.fixture
def mock_chats_repository():
    return MagicMock()


@pytest.fixture
def mock_connection_repository():
    return MagicMock()


test_user = User('some_user_id', 'some_username', 'some_first', 'some_last')


def test_create_chat_id():
    result = create_chat_id()
    assert isinstance(result, str)


@patch('incollege.repositories.UserRepository.get_user')
@patch('incollege.repositories.ChatsRepository.get_chat_by_both_users')
@patch('incollege.repositories.ChatsRepository.create_chat')
def test_create_chat_valid(mock_create_chat, mock_get_chat_by_both_users, mock_get_user, mock_user_repository,
                           mock_chats_repository, mock_connection_repository):
    mock_user_repository.get_user.return_value = MagicMock(tier='standard', first_name='John', last_name='Doe')
    mock_get_chat_by_both_users.return_value = None
    create_chat('user1', 'user2')
    assert mock_create_chat.called


@patch('incollege.repositories.UserRepository.get_user', return_value=None)
def test_create_chat_invalid_user1(mock_get_user, mock_user_repository, mock_chats_repository,
                                   mock_connection_repository):
    with pytest.raises(ContentException):
        create_chat('user1', 'user2')


@patch('incollege.repositories.UserRepository.get_user')
@patch('incollege.repositories.ChatsRepository.get_chat_by_both_users', return_value=True)
def test_create_chat_existing_chat(mock_get_chat_by_both_users, mock_get_user, mock_user_repository,
                                   mock_chats_repository, mock_connection_repository):
    mock_user_repository.get_user.return_value = MagicMock(tier='standard', first_name='John', last_name='Doe')
    with pytest.raises(ContentException):
        create_chat('user1', 'user2')


@patch('incollege.repositories.UserRepository.get_user')
@patch('incollege.repositories.ChatsRepository.get_chat_by_both_users')
def test_create_chat_not_connected(mock_get_chat_by_both_users, mock_get_user,
                                   mock_user_repository, mock_chats_repository, mock_connection_repository):
    mock_user_repository.get_user.return_value = test_user
    mock_get_chat_by_both_users.return_value = N
    mock_connection_repository.connection_check.return_value = False
    with pytest.raises(ContentException):
        create_chat('user1', 'user2')


@patch('incollege.repositories.ChatsRepository.get_chats_by_user')
def test_get_chat_list_valid(mock_get_chats_by_user, mock_user_repository, mock_chats_repository):
    mock_get_chats_by_user.return_value = ['chat1', 'chat2']
    result = get_chat_list('user1')
    assert result == ['chat1', 'chat2']


@patch('incollege.repositories.ChatsRepository.get_chats_by_user', return_value=None)
def test_get_chat_list_no_chats(mock_get_chats_by_user, mock_user_repository, mock_chats_repository):
    with pytest.raises(ContentException):
        get_chat_list('user1')


@patch('incollege.repositories.ChatsRepository.get_chat', return_value='chat')
def test_get_chat_valid(mock_get_chat, mock_chats_repository):
    result = get_chat('chat_id')
    assert result == 'chat'


@patch('incollege.repositories.ChatsRepository.get_chat', return_value=None)
def test_get_chat_invalid(mock_get_chat, mock_chats_repository):
    with pytest.raises(ContentException):
        get_chat('chat_id')
