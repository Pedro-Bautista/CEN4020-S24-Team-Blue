import pytest
from unittest.mock import MagicMock, patch
from incollege.exceptions import ContentException
from incollege.services.ConnectionsService import *


@pytest.fixture
def mock_connection_repository():
    return MagicMock()


@pytest.fixture
def mock_user_repository():
    return MagicMock()


@patch('incollege.repositories.UserRepository.get_user',
       side_effect=[MagicMock(), MagicMock(), None, MagicMock(), None])
@patch('incollege.repositories.ConnectionRepository.get_request_by_sender_and_recipient_user_id',
       return_value=None)
@patch('incollege.repositories.ConnectionRepository.create_connection_request')
def test_send_connection_request(mock_create_connection_request, mock_get_request, mock_get_user,
                                 mock_connection_repository, mock_user_repository):
    # Case 1: Successful request creation
    mock_get_request.return_value = None
    mock_get_user.side_effect = [MagicMock(), MagicMock()]
    send_connection_request('sender_user_id', 'recipient_user_id')
    assert mock_create_connection_request.called

    # Case 2: Sender and recipient are the same
    with pytest.raises(ContentException):
        send_connection_request('same_user_id', 'same_user_id')

    # Case 3: Missing sender user
    mock_get_user.side_effect = [None, MagicMock()]
    with pytest.raises(ContentException):
        send_connection_request('nonexistent_sender_id', 'recipient_user_id')

    # Case 4: Missing recipient user
    mock_get_user.side_effect = [MagicMock(), None]
    with pytest.raises(ContentException):
        send_connection_request('sender_user_id', 'nonexistent_recipient_id')

    # Case 5: Connection request already exists
    mock_get_user.side_effect = [MagicMock(), MagicMock()]
    mock_get_request.return_value = MagicMock()
    with pytest.raises(ContentException):
        send_connection_request('sender_user_id', 'recipient_user_id')

    # Case 6: Missing sender user ID
    with pytest.raises(ContentException):
        send_connection_request('', 'recipient_user_id')

    # Case 7: Missing recipient user ID
    with pytest.raises(ContentException):
        send_connection_request('sender_user_id', '')


@patch('incollege.repositories.ConnectionRepository.get_pending_requests_by_recipient_user_id',
       return_value=['request1', 'request2'])
def test_get_pending_requests_by_recipient_user_id(mock_get_pending_requests, mock_connection_repository):
    result = get_pending_requests_by_recipient_user_id('recipient_user_id')
    assert result == ['request1', 'request2']


@patch('incollege.repositories.ConnectionRepository.get_pending_requests_by_recipient_user_id', return_value=None)
def test_get_pending_requests_by_recipient_user_id_no_requests(mock_get_pending_requests, mock_connection_repository):
    with pytest.raises(ContentException):
        get_pending_requests_by_recipient_user_id('recipient_user_id')


@patch('incollege.repositories.ConnectionRepository.get_connections_by_user_id',
       return_value=['connection1', 'connection2'])
def test_get_connections_by_user_id(mock_get_connections, mock_connection_repository):
    result = get_connections_by_user_id('user_id')
    assert result == ['connection1', 'connection2']


@patch('incollege.repositories.ConnectionRepository.get_connections_by_user_id', return_value=None)
def test_get_connections_by_user_id_no_connections(mock_get_connections, mock_connection_repository):
    with pytest.raises(ContentException):
        get_connections_by_user_id('user_id')


@patch('incollege.repositories.UserRepository.get_connection_users_by_user_id', return_value=['profile1', 'profile2'])
def test_get_connection_profiles_by_user_id(mock_get_connection_profiles, mock_user_repository):
    result = get_connection_profiles_by_user_id('user_id')
    assert result == ['profile1', 'profile2']


@patch('incollege.repositories.UserRepository.get_connection_users_by_user_id', return_value=None)
def test_get_connection_profiles_by_user_id_no_profiles(mock_get_connection_profiles, mock_user_repository):
    with pytest.raises(ContentException):
        get_connection_profiles_by_user_id('user_id')


@patch('incollege.repositories.ConnectionRepository.get_request_by_sender_and_recipient_user_id',
       return_value=MagicMock(status='PENDING'))
@patch('incollege.repositories.ConnectionRepository.update_connection_request')
def test_update_connection_request(mock_update_connection_request, mock_get_request,
                                   mock_connection_repository):
    update_connection_request('sender_user_id', 'recipient_user_id', 'ACCEPTED')
    assert mock_update_connection_request.called
