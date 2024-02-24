from unittest import mock
import pytest

from incollege.entity.User import User
from incollege.services.UserService import *


test_user = User('some_user_id', 'some_username', 'some_first', 'some_last')


@mock.patch('incollege.repositories.UserRepository.search_users_by_name', return_value=[])
def test_find_users_by_name_none(mock_search_users_by_name):
    with pytest.raises(ContentException) as e:
        result = find_users_by_name('some_first', 'some_last')

        assert e == ContentException('No matching users found.', 404)

@mock.patch('incollege.repositories.UserRepository.search_users_by_name', return_value=[test_user])
def test_find_users_by_name(mock_search_users_by_name):
    result = find_users_by_name('some_first', 'some_last')

    assert result == [test_user]

@mock.patch('incollege.repositories.UserRepository.get_user', return_value=None)
def test_update_preference_no_user(mock_get_user):
    with pytest.raises(ContentException) as e:
        result = update_preference('some_user_id', 'some_pref_name', 'some_pref_value')

        assert e == ContentException('No such user.', 404)

@mock.patch('incollege.repositories.UserRepository.get_user', return_value=test_user)
def test_update_preference_no_such_pref(mock_get_user):
    with pytest.raises(ContentException) as e:
        result = update_preference('some_user_id', 'invalid_pref_name', 'some_pref_value')

        assert e == ContentException('No such preference.', 404)

@mock.patch('incollege.repositories.UserRepository.get_user', return_value=test_user)
@mock.patch('incollege.repositories.UserRepository.update_user')
def test_update_preference(mock_update_user, mock_get_user):
    result = update_preference('some_user_id', 'language_pref', 'some_pref_value')
