from unittest import mock

from incollege.repositories.AuthRepository import *

auth_user_description = (
    ('user_id',),
    ('username',),
    ('password_hash',),
    ('permissions_group',)
)
test_auth_user_data = [
    ('some_uuid', 'some_username', 'some_hash', 'some_group')
]
test_auth_user = AuthUser(**dict(zip([key[0] for key in auth_user_description], test_auth_user_data[0])))


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_user_count(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, )

    result = get_auth_user_count()

    assert result == 1


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_user_id_none(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = ()
    mock_cursor.description = auth_user_description

    result = get_user_id(test_auth_user.username)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_user_id(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = test_auth_user_data
    mock_cursor.description = auth_user_description

    result = get_user_id(test_auth_user.username)

    assert result == test_auth_user.user_id


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_permissions_group_none(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = ()
    mock_cursor.description = auth_user_description

    result = get_permissions_group(test_auth_user.user_id)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_permissions_group(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = test_auth_user_data
    mock_cursor.description = auth_user_description

    result = get_permissions_group(test_auth_user.user_id)

    assert result == test_auth_user.permissions_group


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_password_hash_none(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = ()
    mock_cursor.description = auth_user_description

    result = get_password_hash(test_auth_user.username)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_password_hash(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = test_auth_user_data
    mock_cursor.description = auth_user_description

    result = get_password_hash(test_auth_user.user_id)

    assert result == test_auth_user.password_hash


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_create_auth_user(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = create_auth_user(test_auth_user)

    assert result is None
