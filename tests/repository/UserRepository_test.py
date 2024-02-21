from unittest import mock

from incollege.repositories.UserRepository import *

user_description = (
    ('user_id',),
    ('username',),
    ('first_name',),
    ('last_name',),
    ('language_pref',),
    ('email_pref',),
    ('sms_pref',),
    ('targeted_adv_pref',)
)
test_user_data = [
    ('some_uuid', 'some_username', 'some_first_name', 'some_last_name', 'some_language', 'some_email_pref',
     'some_sms_pref', 'some_targeted_adv_pref')
]
test_user_data2 = [
    ('some_uuid2', 'some_username2', 'some_first_name2', 'some_last_name2', 'some_language2', 'some_email_pref2',
     'some_sms_pref2', 'some_targeted_adv_pref2')
]
test_user = User(**dict(zip([key[0] for key in user_description], test_user_data[0])))
test_user2 = User(**dict(zip([key[0] for key in user_description], test_user_data2[0])))

@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_create_user(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = create_user(test_user)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_user_none(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = ()

    result = get_user(test_user.user_id)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_user(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = test_user_data
    mock_cursor.description = user_description

    result = get_user(test_user.user_id)

    assert vars(result) == vars(test_user)


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_search_users_by_name_none(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = ()
    mock_cursor.description = user_description

    result = search_users_by_name(test_user.first_name, test_user.last_name)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_search_users_by_name(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [test_user_data, test_user_data2]
    mock_cursor.description = user_description

    result = search_users_by_name(test_user.first_name, test_user.last_name)

    assert len(result) == 2


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_update_user(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = update_user(test_user)

    assert result is None
