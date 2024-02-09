import json
import os

import pytest
from flask import Flask, request

from incollege.config import Config
from incollege.controllers.AuthController import *
from incollege.controllers.ControllerAdvice import configure_controller_advice
from incollege.repositories.DBConnector import create_tables


@pytest.fixture(scope='module')
def test_client():
    test_app = Flask(__name__)
    test_app.config['TESTING'] = True
    configure_auth_routes(test_app)
    configure_controller_advice(test_app)

    print('Attempting to reset database...')
    try:
        os.remove(Config.DATABASE_NAME)
        print('Successfully deleted existing test database.')
    except FileNotFoundError:
        print('Test database not found. Creating...')
    create_tables()
    print('Created new test database.')

    with test_app.test_client() as test_client:
        with test_app.app_context():
            yield test_client


# User 1 -> austin
def test_001_handle_signup_valid(test_client):
    data = {'username': 'austin', 'password': '@W93GW1s&0GO'}
    response = test_client.post('/signup', json=data)

    assert response.status_code == 201

    verify_token_exists(response)
    verify_login(test_client, data)


def test_002_handle_signup_duplicate_user_failed(test_client):
    data = {'username': 'austin', 'password': '54a8&9$HM@'}

    response = test_client.post('/signup', json=data)
    verify_expected_error(response, 'Username already exists.', 409)


def test_003_handle_login_valid_password(test_client):
    data = {'username': 'austin', 'password': '@W93GW1s&0GO'}
    response = test_client.post('/login', json=data)

    assert response.status_code == 200

    verify_token_exists(response)


def test_004_handle_login_invalid_password(test_client):
    data = {'username': 'austin', 'password': 'invalid_password'}
    response = test_client.post('/login', json=data)
    verify_expected_error(response, 'Invalid username or password.', 401)


# User 2 -> clifford
def test_005_handle_signup_valid_create_test_user2(test_client):
    data = {'username': 'clifford', 'password': '?0y8~16Nfhg%'}
    response = test_client.post('/signup', json=data)
    assert response.status_code == 201

    verify_token_exists(response)
    verify_login(test_client, data)


# User 3 -> T-Bone
def test_006_handle_signup_valid_create_test_user3(test_client):
    data = {'username': 'T-Bone', 'password': '1oT;8Jg5J3w4'}
    response = test_client.post('/signup', json=data)
    assert response.status_code == 201

    verify_token_exists(response)
    verify_login(test_client, data)


# User 4 -> Cleo
def test_007_handle_signup_valid_create_test_user4(test_client):
    data = {'username': 'Cleo', 'password': '988a8&9#HM@'}
    response = test_client.post('/signup', json=data)
    assert response.status_code == 201

    verify_token_exists(response)
    verify_login(test_client, data)


# User 5 -> Machiavelli
def test_008_handle_signup_valid_create_test_user5(test_client):
    data = {'username': 'Machiavelli', 'password': '18v3@8Q3"j|X'}
    response = test_client.post('/signup', json=data)
    assert response.status_code == 201

    verify_token_exists(response)
    verify_login(test_client, data)


def test_009_handle_signup_max_users_reached(test_client):
    data = {'username': 'Hamburger', 'password': 'DOFp6(YF%22u'}
    response = test_client.post('/signup', json=data)
    verify_expected_error(response, 'User limit reached.', 507)


def verify_login(test_client, data):
    response = test_client.post('/login', json=data)
    assert response.status_code == 200


def verify_token_exists(response):
    assert json.loads(response.get_data(as_text=True)) is not None
    assert json.loads(response.get_data(as_text=True))['token'] is not None


def verify_expected_error(response, expected, expected_http_code=None):
    actual = json.loads(response.data)['error']['description']
    assert expected == actual
    if expected is not None:
        assert response.status_code == expected_http_code
