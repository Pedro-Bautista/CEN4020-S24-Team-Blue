from unittest import mock

import pytest

import os

import sys

# ---------- path config --------------------------------------------------------------------#
# Get the parent directory of the current directory (tests/controllers/integration)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Add the parent directory to the Python path
sys.path.append(parent_dir)
# ---------- path config --------------------------------------------------------------------#


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


@mock.patch('incollege.repositories.AuthRepository.get_password_hash', return_value="TEST_HASH")
@mock.patch('incollege.services.AuthService.hash_password', return_value='WRONG_HASH')
@mock.patch('incollege.services.AuthService.create_token', return_value='INVALID_TOKEN')
def test_login_failed(mock_create_token, mock_hash_password, mock_get_password_hash):
    with pytest.raises(AuthException):
        login('austin', 'wrong password')

    mock_get_password_hash.assert_called_once_with('austin')
    mock_hash_password.assert_called_once_with('wrong password')
    mock_create_token.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.get_password_hash', return_value="TEST_HASH")
@mock.patch('incollege.services.AuthService.hash_password', return_value='TEST_HASH')
@mock.patch('incollege.services.AuthService.create_token', return_value='VALID_TOKEN')
def test_login_success(mock_create_token, mock_hash_password, mock_get_password_hash):
    result = login("austin", "correct password")

    assert result is not None
    mock_get_password_hash.assert_called_once_with('austin')
    mock_hash_password.assert_called_once_with('correct password')
    mock_create_token.assert_called_once_with('austin')


@mock.patch('incollege.repositories.AuthRepository.get_password_hash', return_value="TEST_HASH")
@mock.patch('incollege.services.AuthService.hash_password', return_value='')
@mock.patch('incollege.services.AuthService.create_token', return_value='INVALID_TOKEN')
def test_login_no_input(mock_create_token, mock_hash_password, mock_get_password_hash):
    with pytest.raises(AuthException) as e_info:
        login('', 'this')
        assert e_info.value == 'Username or password not provided.'
    mock_get_password_hash.assert_not_called()
    mock_hash_password.assert_not_called()
    mock_create_token.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.get_password_hash', return_value="TEST_HASH")
@mock.patch('incollege.services.AuthService.hash_password', return_value='')
@mock.patch('incollege.services.AuthService.create_token', return_value='INVALID_TOKEN')
def test_login_no_input(mock_create_token, mock_hash_password, mock_get_password_hash):
    with pytest.raises(AuthException) as e_info:
        login('this', '')
        assert e_info.value == 'Username or password not provided.'
    mock_get_password_hash.assert_not_called()
    mock_hash_password.assert_not_called()
    mock_create_token.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.get_password_hash', return_value="TEST_HASH")
@mock.patch('incollege.services.AuthService.hash_password', return_value='')
@mock.patch('incollege.services.AuthService.create_token', return_value='INVALID_TOKEN')
def test_login_no_input(mock_create_token, mock_hash_password, mock_get_password_hash):
    with pytest.raises(AuthException) as e_info:
        login('', '')
        assert e_info.value == 'Username or password not provided.'
    mock_get_password_hash.assert_not_called()
    mock_hash_password.assert_not_called()
    mock_create_token.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.create_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_user_count', return_value=Config.USER_LIMIT - 1)
@mock.patch('incollege.repositories.AuthRepository.user_exists', return_value=False)
def test_signup_success(mock_user_exists, mock_get_user_count, mock_create_user):
    result = signup('austin', 'vAl1d-p@ss', 'austin', 'holmes')

    assert result is not None
    mock_user_exists.assert_called_once_with('austin')
    mock_get_user_count.assert_called_once()
    mock_create_user.assert_called_once_with('austin', hash_password('vAl1d-p@ss'), 'austin', 'holmes')


@mock.patch('incollege.repositories.AuthRepository.create_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_user_count', return_value=Config.USER_LIMIT - 1)
@mock.patch('incollege.repositories.AuthRepository.user_exists', return_value=False)
def test_signup_no_password(mock_user_exists, mock_get_user_count, mock_create_user):
    with pytest.raises(AuthException) as e_info:
        signup('austin', '', 'austin', 'holmes')
        assert e_info.value == 'Username or password not provided.'
    mock_user_exists.assert_not_called()
    mock_get_user_count.assert_not_called()
    mock_create_user.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.create_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_user_count', return_value=Config.USER_LIMIT - 1)
@mock.patch('incollege.repositories.AuthRepository.user_exists', return_value=False)
def test_signup_no_username(mock_user_exists, mock_get_user_count, mock_create_user):
    with pytest.raises(AuthException) as e_info:
        signup('', 'vAl1d-p@ss', 'austin', 'holmes')
        assert e_info.value == 'Username or password not provided.'
    mock_user_exists.assert_not_called()
    mock_get_user_count.assert_not_called()
    mock_create_user.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.create_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_user_count', return_value=Config.USER_LIMIT - 1)
@mock.patch('incollege.repositories.AuthRepository.user_exists', return_value=False)
def test_signup_invalid_password(mock_user_exists, mock_get_user_count, mock_create_user):
    with pytest.raises(AuthException) as e_info:
        signup('austin', 'password', 'austin', 'holmes')
        assert e_info.value == 'Password does not meet requirements.'
    mock_user_exists.assert_not_called()
    mock_get_user_count.assert_not_called()
    mock_create_user.assert_not_called()


@mock.patch('incollege.repositories.AuthRepository.create_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_user_count', return_value=Config.USER_LIMIT - 1)
@mock.patch('incollege.repositories.AuthRepository.user_exists', return_value=True)
def test_signup_user_exists(mock_user_exists, mock_get_user_count, mock_create_user):
    with pytest.raises(AuthException) as e_info:
        signup('austin', 'vAl1d-p@ss', 'austin', 'holmes')
        assert e_info.value == 'Username already exists.'
    mock_user_exists.assert_called_once_with('austin')
    mock_get_user_count.assert_not_called()
    mock_create_user.assert_not_called()


# ----------------------------------------------------------------------------------------------------------------
# signup extended
    
@mock.patch('incollege.repositories.AuthRepository.create_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_user_count', return_value=Config.USER_LIMIT - 1)
@mock.patch('incollege.repositories.AuthRepository.user_exists', return_value=True)
def test_signup_no_name(mock_user_exists, mock_get_user_count, mock_create_user):
    with pytest.raises(AuthException) as e_info:
        signup('austin', 'vAl1d-p@ss', '', '')
        assert e_info.value == 'First or last name are not provided.'
    mock_get_user_count.assert_not_called()
    mock_create_user.assert_not_called()



# ----------------------------------------------------------------------------------------------------------------

@mock.patch('incollege.repositories.AuthRepository.create_user', return_value='SOME_TOKEN')
@mock.patch('incollege.repositories.AuthRepository.get_user_count', return_value=Config.USER_LIMIT)
@mock.patch('incollege.repositories.AuthRepository.user_exists', return_value=False)
def test_signup_user_limit_reached(mock_user_exists, mock_get_user_count, mock_create_user):
    with pytest.raises(AuthException) as e_info:
        signup('austin', 'vAl1d-p@ss', 'austin', 'holmes')
        assert e_info.value == 'User limit reached.'
    mock_user_exists.assert_called_once_with('austin')
    mock_get_user_count.assert_called_once()
    mock_create_user.assert_not_called()


def test_create_token():
    result = create_token('austin')
    reference_payload = {
        'usr': 'austin',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Config.TOKEN_DURATION)
    }
    reference_token = jwt.encode(reference_payload, Config.SECRET, algorithm='HS512')

    assert result == reference_token


def test_decode_token():
    reference_payload = {
        'usr': 'austin',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Config.TOKEN_DURATION)
    }
    reference_token = jwt.encode(reference_payload, Config.SECRET, algorithm='HS512')
    result = decode_token(reference_token)

    assert result['usr'] == 'austin'
