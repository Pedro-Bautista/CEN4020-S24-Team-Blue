import json
from unittest import mock
import pytest
from flask import Flask

from incollege.controllers.AuthController import configure_auth_routes
from incollege.exceptions.AuthException import AuthException


@pytest.fixture(scope='module')
def test_client():
    test_app = Flask(__name__)
    test_app.config['TESTING'] = True
    configure_auth_routes(test_app)

    with test_app.test_client() as test_client:
        with test_app.app_context():
            yield test_client

def test_index_route(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'Welcome to InCollege!'

@mock.patch('incollege.services.AuthService.login', return_value='mocked_token')
def test_handle_login_route_success(mock_login, test_client):
    data = {'username': 'test_user', 'password': 'test_password', 'first_name': 'austin', 'last_name': 'holmes'}
    response = test_client.post('/login', json=data)

    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == {'token': 'mocked_token'}
    mock_login.assert_called_once_with('test_user', 'test_password')

@mock.patch('incollege.services.AuthService.signup', return_value='mocked_token')
def test_handle_signup_route_success(mock_signup, test_client):
    data = {'username': 'test_user', 'password': 'test_password', 'first_name': 'austin', 'last_name': 'holmes'}
    response = test_client.post('/signup', json=data)

    assert response.status_code == 201
    assert json.loads(response.get_data(as_text=True)) == {'token': 'mocked_token'}
    mock_signup.assert_called_once_with('test_user', 'test_password', 'austin', 'holmes')


@mock.patch('incollege.services.AuthService.login', side_effect=AuthException('Invalid username or password.'))
def test_handle_login_route_error(mock_login, test_client):
    data = {'username': 'test_user', 'password': 'test_password', 'first_name': 'austin', 'last_name': 'holmes'}
    with pytest.raises(AuthException) as e_info:
        test_client.post('/login', json=data)
        assert e_info.value == 'Invalid username or password.'
    mock_login.assert_called_once_with('test_user', 'test_password')



@mock.patch('incollege.services.AuthService.signup', side_effect=AuthException('Username already exists.'))
def test_handle_signup_route_error(mock_signup, test_client):
    data = {'username': 'test_user', 'password': 'test_password', 'first_name': 'austin', 'last_name': 'holmes'}
    with pytest.raises(AuthException) as e_info:
        test_client.post('/signup', json=data)
        assert e_info.value == 'Username already exists.'
    mock_signup.assert_called_once_with('test_user', 'test_password', 'austin', 'holmes')
