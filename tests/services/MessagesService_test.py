import pytest
from unittest.mock import patch, MagicMock
from incollege.exceptions.ContentException import ContentException
from incollege.services.MessagesService import create_message, get_messages, delete_message, change_read_status, \
    get_unread


@pytest.fixture
def mock_get_user():
    return MagicMock()


@pytest.fixture
def mock_get_chat():
    return MagicMock()


@pytest.fixture
def mock_get_message():
    return MagicMock()


@pytest.fixture
def mock_messages_repository():
    return MagicMock()


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.ChatsRepository.get_chat', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.get_messages_by_chat_id', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.create_message')
def test_create_message_success(mock_create_message, mock_get_messages_by_chat_id, mock_get_chat, mock_get_user):
    create_message('user1', 'chat_id', 'Hello')
    assert mock_create_message.called


@patch('incollege.repositories.UserRepository.get_user', return_value=None)
def test_create_message_missing_user(mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        create_message('', 'chat_id', 'Hello')
    assert str(exc_info.value) == 'No such user.'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.ChatsRepository.get_chat', return_value=None)
def test_create_message_missing_chat(mock_get_chat, mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        create_message('user1', '', 'Hello')
    assert str(exc_info.value) == 'Required message information not provided.'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.ChatsRepository.get_chat', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.get_messages_by_chat_id', return_value=MagicMock())
def test_create_message_content_limit(mock_get_messages_by_chat_id, mock_get_chat, mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        create_message('user1', 'chat_id', 'a' * 1001)
    assert str(exc_info.value) == 'Message content must not exceed 1000 characters'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.ChatsRepository.get_chat', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.get_messages_by_chat_id', return_value=MagicMock())
def test_get_messages_success(mock_get_messages_by_chat_id, mock_get_chat, mock_get_user):
    result = get_messages('user1', 'chat_id')
    assert result == mock_get_messages_by_chat_id.return_value


@patch('incollege.repositories.UserRepository.get_user', return_value=None)
def test_get_messages_missing_user(mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        get_messages('', 'chat_id')
    assert str(exc_info.value) == 'Cannot get messages with information provided.'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.ChatsRepository.get_chat', return_value=None)
def test_get_messages_missing_chat(mock_get_chat, mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        get_messages('user1', '')
    assert str(exc_info.value) == 'Cannot get messages with information provided.'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.get_message', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.delete_message')
def test_delete_message_success(mock_delete_message, mock_get_message, mock_get_user):
    delete_message('user1', 'message_id')
    assert mock_delete_message.called


@patch('incollege.repositories.UserRepository.get_user', return_value=None)
def test_delete_message_missing_user(mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        delete_message('', 'message_id')
    assert str(exc_info.value) == 'Cannot delete messages with information provided.'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.get_message', return_value=None)
def test_delete_message_missing_message(mock_get_message, mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        delete_message('user1', 'message_id')
    assert str(exc_info.value) == 'No such message.'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.get_message', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.change_read_status')
def test_change_read_status_success(mock_change_read_status, mock_get_message, mock_get_user):
    change_read_status('user1', 'chat_id', 'message_id', 'READ')
    assert mock_change_read_status.called


@patch('incollege.repositories.UserRepository.get_user', return_value=None)
def test_change_read_status_missing_user(mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        change_read_status('', 'chat_id', 'message_id', 'READ')
    assert str(exc_info.value) == 'Cannot change status with information provided'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.get_message', return_value=None)
def test_change_read_status_missing_message(mock_get_message, mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        change_read_status('user1', 'chat_id', 'message_id', 'READ')
    assert str(exc_info.value) == 'Message does not exist.'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.get_message', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.change_read_status')
def test_change_read_status_missing_status(mock_change_read_status, mock_get_message, mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        change_read_status('user1', 'chat_id', 'message_id', '')
    assert str(exc_info.value) == 'Cannot change status with information provided'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.get_message', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.change_read_status')
def test_change_read_status_status_update(mock_change_read_status, mock_get_message, mock_get_user):
    change_read_status('user1', 'chat_id', 'message_id', 'READ')
    assert mock_change_read_status.called


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.ChatsRepository.get_chat', return_value=MagicMock())
@patch('incollege.repositories.MessagesRepository.get_unread', return_value=MagicMock())
def test_get_unread_status_update(mock_get_unread, mock_get_chat, mock_get_user):
    with patch('incollege.repositories.MessagesRepository.change_read_status') as mock_change_read_status:
        get_unread('user1', 'chat_id')
        assert mock_get_unread.called
