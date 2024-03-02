import json
from unittest import mock
import pytest
from flask import Flask

from incollege.controllers.ControllerAdvice import configure_controller_advice
from incollege.controllers.UserController import configure_user_routes
from incollege.entity.User import User
from incollege.exceptions.ContentException import ContentException
from incollege.services import AuthService

test_user1 = User('some_user_id', 'some_username', 'some_first', 'some_last')
test_user2 = User('some_user_id2', 'some_username2', 'some_first2', 'some_last2')
test_jwt_header = {'token': AuthService.create_token('some_user_id', 'user')}
test_invalid_jwt_header = {'token': 'invalid_token'}

@pytest.fixture(scope='module')
def test_client():
    test_app = Flask(__name__)
    test_app.config['TESTING'] = True
    configure_user_routes(test_app)
    configure_controller_advice(test_app)

    with test_app.test_client() as test_client:
        with test_app.app_context():
            yield test_client


@mock.patch('incollege.services.UserService.search_users', return_value=[test_user1, test_user2])
def test_handle_user_search_success(mock_search_users, test_client):
    data = {'first_name': 'some_first', 'last_name': 'some_last'}
    response = test_client.post('/user_search', json=data)

    assert response.status_code == 200
    assert get_response_message(response) == [vars(test_user1), vars(test_user2)]


@mock.patch('incollege.services.UserService.search_users',
            side_effect=ContentException('No matching users found.', 404))
def test_handle_user_search_error(mock_search_users, test_client):
    data = {'first_name': 'some_first', 'last_name': 'some_last'}
    response = test_client.post('/user_search', json=data)

    assert response.status_code == 404
    assert get_response_error_desc(response) == 'No matching users found.'


def test_handle_user_search_malformed(test_client):
    data = {'malformed': 'yep'}
    response = test_client.post('/user_search', json=data)

    assert response.status_code == 400
    assert get_response_error_desc(response) == 'Required search parameters not provided.'


@mock.patch('incollege.services.UserService.update_preference')
def test_handle_update_preference_success(mock_update_preference, test_client):
    data = {'preference_name': 'some_preference_name', 'preference_value': 'some_preference_value'}
    response = test_client.post('/update_preferences', json=data, headers=test_jwt_header)

    assert response.status_code == 200


@mock.patch('incollege.services.UserService.update_preference')
def test_handle_update_preference_unauthorized(mock_update_preference, test_client):
    data = {'preference_name': 'some_preference_name', 'preference_value': 'some_preference_value'}
    response = test_client.post('/update_preferences', json=data, headers=test_invalid_jwt_header)

    assert response.status_code == 401


@mock.patch('incollege.services.UserService.update_preference',
            side_effect=ContentException('Required preference parameters not provided.', 400))
def test_handle_update_preference_malformed(mock_update_preference, test_client):
    data = {'preference_name': 'some_preference_name', 'bad_field': 'some_preference_value'}
    response = test_client.post('/update_preferences', json=data, headers=test_jwt_header)

    assert response.status_code == 400


@mock.patch('incollege.services.UserService.update_preference', side_effect=ContentException('No such user.', 404))
def test_handle_update_preference_error(mock_update_preference, test_client):
    data = {'preference_name': 'some_preference_name', 'preference_value': 'some_preference_value'}
    response = test_client.post('/update_preferences', json=data, headers=test_jwt_header)

    assert response.status_code == 404
    assert get_response_error_desc(response) == 'No such user.'


def get_response_error_desc(response):
    return json.loads(response.data)['error']['description']


def get_response_message(response):
    return json.loads(response.data)['message']
