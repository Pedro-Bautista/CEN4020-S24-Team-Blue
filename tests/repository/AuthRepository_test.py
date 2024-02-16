from unittest import mock

from incollege.repositories.AuthRepository import *


@mock.patch('incollege.repositories.AuthRepository.get_connection')
def test_get_user_count(mock_get_connection):
    mock_cursor = mock_get_connection.return_value.cursor.return_value
    mock_cursor.execute.return_value.fetchone.return_value = (3, )

    result = get_auth_user_count()

    assert result == 3


@mock.patch('incollege.repositories.AuthRepository.get_connection')
def test_get_user_count(mock_get_connection):
    mock_cursor = mock_get_connection.return_value.cursor.return_value
    mock_cursor.execute.return_value.fetchone.return_value = ('some_hash',)

    result = get_password_hash('austin')

    assert result == 'some_hash'


@mock.patch('incollege.repositories.AuthRepository.get_connection')
def test_user_exists_true(mock_get_connection):
    mock_cursor = mock_get_connection.return_value.cursor.return_value
    mock_cursor.execute.return_value.fetchone.return_value = (1, )

    result = auth_user_exists('austin')

    assert result is True


@mock.patch('incollege.repositories.AuthRepository.get_connection')
def test_user_exists_false(mock_get_connection):
    mock_cursor = mock_get_connection.return_value.cursor.return_value
    mock_cursor.execute.return_value.fetchone.return_value = (0, )

    result = auth_user_exists('austin')

    assert result is False


@mock.patch('incollege.repositories.AuthRepository.get_connection')
def test_user_exists_false(mock_get_connection):
    mock_cursor = mock_get_connection.return_value.cursor.return_value

    create_auth_user('austin', 'some_hash')


@mock.patch('incollege.repositories.AuthRepository.get_connection')
def test_user_exists_false(mock_get_connection):
    mock_cursor = mock_get_connection.return_value.cursor.return_value

    delete_auth_user('austin')
