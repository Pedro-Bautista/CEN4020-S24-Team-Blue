from unittest import mock
import pytest

from incollege.services.AuthService import *


def test_invalid_password():
    result = validate_password('invalid password')

    assert result is False


def test_valid_password():
    result = validate_password('vAl1d-p@ss')

    assert result is True


def test_hash_password():
    result = hash_password('test-input')

    assert result == 'd940e918aa66b827708f1391f562894382cc29341a3c190368b2cce82a6bdf32d060b065bb4ea73c8b1d' \
                     '956de5b75fe4113db81b7268cf7f2ae9ba563fbe5c5e'


@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value="TEST_USER_ID")
@mock.patch('incollege.repositories.AuthRepository.get_permissions_group', return_value="TEST_GROUP")
@mock.patch('incollege.repositories.AuthRepository.get_password_hash', return_value="TEST_HASH")
@mock.patch('incollege.services.AuthService.hash_password', return_value='WRONG_HASH')
@mock.patch('incollege.entity.AuthJWT.AuthJWT.encode', return_value='INVALID_TOKEN')
def test_login_failed(mock_create_token, mock_hash_password, mock_get_password_hash,
                      mock_get_permissions_group, mock_get_user_id):
    with pytest.raises(AuthException):
        login('austin', 'wrong password')

    mock_create_token.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value="TEST_USER_ID")
@mock.patch('incollege.repositories.AuthRepository.get_permissions_group', return_value="TEST_GROUP")
@mock.patch('incollege.repositories.AuthRepository.get_password_hash', return_value="TEST_HASH")
@mock.patch('incollege.services.AuthService.hash_password', return_value='TEST_HASH')
@mock.patch('incollege.entity.AuthJWT.AuthJWT.encode', return_value='VALID_TOKEN')
def test_login_success(mock_create_token, mock_hash_password, mock_get_password_hash,
                       mock_get_permissions_group, mock_get_user_id):
    result = login("austin", "correct password")

    assert result is not None

    mock_create_token.assert_called_once()


@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value="TEST_USER_ID")
@mock.patch('incollege.repositories.AuthRepository.get_permissions_group', return_value="TEST_GROUP")
@mock.patch('incollege.repositories.AuthRepository.get_password_hash', return_value="TEST_HASH")
@mock.patch('incollege.services.AuthService.hash_password', return_value='')
@mock.patch('incollege.entity.AuthJWT.AuthJWT.encode', return_value='INVALID_TOKEN')
def test_login_no_username(mock_create_token, mock_hash_password, mock_get_password_hash,
                           mock_get_permissions_group, mock_get_user_id):
    with pytest.raises(AuthException) as e_info:
        login('', 'this')
        assert e_info.value == 'Username or password not provided.'

    mock_create_token.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value="TEST_USER_ID")
@mock.patch('incollege.repositories.AuthRepository.get_permissions_group', return_value="TEST_GROUP")
@mock.patch('incollege.repositories.AuthRepository.get_password_hash', return_value="TEST_HASH")
@mock.patch('incollege.services.AuthService.hash_password', return_value='')
@mock.patch('incollege.entity.AuthJWT.AuthJWT.encode', return_value='INVALID_TOKEN')
def test_login_no_password(mock_create_token, mock_hash_password, mock_get_password_hash,
                           mock_get_permissions_group, mock_get_user_id):
    with pytest.raises(AuthException) as e_info:
        login('this', '')
        assert e_info.value == 'Username or password not provided.'

    mock_create_token.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value="TEST_USER_ID")
@mock.patch('incollege.repositories.AuthRepository.get_permissions_group', return_value="TEST_GROUP")
@mock.patch('incollege.repositories.AuthRepository.get_password_hash', return_value="TEST_HASH")
@mock.patch('incollege.services.AuthService.hash_password', return_value='')
@mock.patch('incollege.entity.AuthJWT.AuthJWT.encode', return_value='INVALID_TOKEN')
def test_login_no_input(mock_create_token, mock_hash_password, mock_get_password_hash,
                        mock_get_permissions_group, mock_get_user_id):
    with pytest.raises(AuthException) as e_info:
        login('', '')
        assert e_info.value == 'Username or password not provided.'

    mock_create_token.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value=None)
@mock.patch('incollege.repositories.UserRepository.create_user')
@mock.patch('incollege.repositories.AuthRepository.create_auth_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_auth_user_count', return_value=Config.USER_LIMIT - 1)
def test_signup_success(mock_get_auth_user_count, mock_create_auth_user, mock_create_user,
                        mock_get_user_id):
    result = signup('austin', 'vAl1d-p@ss', 'austin', 'holmes')

    assert result is not None

    mock_create_auth_user.assert_called_once()
    mock_create_user.assert_called_once()


@mock.patch('incollege.repositories.UserRepository.create_user')
@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value=None)
@mock.patch('incollege.repositories.AuthRepository.create_auth_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_auth_user_count', return_value=Config.USER_LIMIT - 1)
def test_signup_no_password(mock_get_auth_user_count, mock_create_auth_user, mock_get_user_id,
                            mock_create_user):
    with pytest.raises(AuthException) as e:
        signup('austin', '', 'austin', 'holmes')

        assert e == AuthException('Username or password are not provided.')

    mock_create_auth_user.assert_not_called()
    mock_create_user.assert_not_called()


@mock.patch('incollege.repositories.UserRepository.create_user')
@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value=None)
@mock.patch('incollege.repositories.AuthRepository.create_auth_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_auth_user_count', return_value=Config.USER_LIMIT - 1)
def test_signup_no_username(mock_get_auth_user_count, mock_create_auth_user, mock_get_user_id,
                            mock_create_user):
    with pytest.raises(AuthException) as e:
        signup('', 'password', 'austin', 'holmes')

        assert e == AuthException('Username or password are not provided.')

    mock_create_auth_user.assert_not_called()
    mock_create_user.assert_not_called()


@mock.patch('incollege.repositories.UserRepository.create_user')
@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value=None)
@mock.patch('incollege.repositories.AuthRepository.create_auth_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_auth_user_count', return_value=Config.USER_LIMIT - 1)
def test_signup_invalid_password(mock_get_auth_user_count, mock_create_auth_user, mock_get_user_id,
                                 mock_create_user):
    with pytest.raises(AuthException) as e:
        signup('austin', 'invalid-password', 'austin', 'holmes')

        assert e == AuthException('Password does not meet requirements.')

    mock_create_auth_user.assert_not_called()
    mock_create_user.assert_not_called()


@mock.patch('incollege.repositories.UserRepository.create_user')
@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value='SOME_ID')
@mock.patch('incollege.repositories.AuthRepository.create_auth_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_auth_user_count', return_value=Config.USER_LIMIT - 1)
def test_signup_user_exists(mock_get_auth_user_count, mock_create_auth_user, mock_get_user_id,
                            mock_create_user):
    with pytest.raises(AuthException) as e:
        signup('austin', 'VAl1d-p@ss', 'austin', 'holmes')

        assert e == AuthException('Username already exists.')

    mock_create_auth_user.assert_not_called()
    mock_create_user.assert_not_called()


@mock.patch('incollege.repositories.UserRepository.create_user')
@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value=None)
@mock.patch('incollege.repositories.AuthRepository.create_auth_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_auth_user_count', return_value=Config.USER_LIMIT - 1)
def test_signup_no_name(mock_get_auth_user_count, mock_create_auth_user, mock_get_user_id,
                        mock_create_user):
    with pytest.raises(AuthException) as e:
        signup('austin', 'VAlid-p@ss', '', '')

        assert e == AuthException('First or last name are not provided.')

    mock_create_auth_user.assert_not_called()
    mock_create_user.assert_not_called()


@mock.patch('incollege.repositories.UserRepository.create_user')
@mock.patch('incollege.repositories.AuthRepository.get_user_id', return_value=None)
@mock.patch('incollege.repositories.AuthRepository.create_auth_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_auth_user_count', return_value=Config.USER_LIMIT)
def test_signup_user_limit_reached(mock_get_auth_user_count, mock_create_auth_user, mock_get_user_id,
                                   mock_create_user):
    with pytest.raises(AuthException) as e:
        signup('austin', 'VAl1d-p@ss', 'austin', 'holmes')

        assert e == AuthException('User limit reached.')

    mock_create_auth_user.assert_not_called()
    mock_create_user.assert_not_called()
