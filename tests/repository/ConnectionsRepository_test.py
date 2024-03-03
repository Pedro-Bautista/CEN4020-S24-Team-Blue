from unittest import mock, TestCase
from incollege.repositories.ConnectionRepository import *

connection_request_description = (
    ('sender_user_id',),
    ('recipient_user_id',),
    ('status',)
)
test_connection_request_data = [
    ('some_sender_user_id1', 'some_recipient_user_id1', 'some_status1')
]
test_connection_request_data_mutated = [
    ('some_sender_user_id2', 'some_recipient_user_id2', 'some_status2')
]
test_connection_request = ConnectionRequest(**dict(zip([key[0] for key in connection_request_description],
                                                       test_connection_request_data[0])))

test_connection_request_mutated = ConnectionRequest(**dict(zip([key[0] for key in connection_request_description],
                                                               test_connection_request_data_mutated[0])))


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_update_connection(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = update_connection_request(test_connection_request_mutated)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_create_connection_request(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = create_connection_request(test_connection_request)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_requests_by_sender_and_recipient_user_id_none(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = ()
    mock_cursor.description = connection_request_description

    result = get_request_by_sender_and_recipient_user_id(test_connection_request.sender_user_id,
                                                         test_connection_request.recipient_user_id)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_requests_by_sender_and_recipient_user_id(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = test_connection_request_data
    mock_cursor.description = connection_request_description

    result = get_request_by_sender_and_recipient_user_id(test_connection_request.sender_user_id,
                                                         test_connection_request.recipient_user_id)

    assert vars(result) == vars(test_connection_request)


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_pending_requests_by_sender_user_id_none(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = ()
    mock_cursor.description = connection_request_description

    result = get_pending_requests_by_sender_user_id(test_connection_request.sender_user_id)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_pending_requests_by_sender_user_id(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = test_connection_request_data
    mock_cursor.description = connection_request_description

    result = get_pending_requests_by_sender_user_id(test_connection_request.sender_user_id)

    assert len(result) == 1


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_pending_requests_by_recipient_user_id_none(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = ()
    mock_cursor.description = connection_request_description

    result = get_pending_requests_by_recipient_user_id(test_connection_request.recipient_user_id)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_pending_requests_by_recipient_user_id(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = test_connection_request_data
    mock_cursor.description = connection_request_description

    result = get_pending_requests_by_recipient_user_id(test_connection_request.recipient_user_id)

    assert len(result) == 1

@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_connections_by_user_id_none(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = ()
    mock_cursor.description = connection_request_description

    result = get_connections_by_user_id(test_connection_request.sender_user_id)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_connections_by_user_id(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = test_connection_request_data
    mock_cursor.description = connection_request_description

    result = get_connections_by_user_id(test_connection_request.sender_user_id)

    # Same fetchall value used twice - testing limitation; result would actually be 1
    assert len(result) == 2
