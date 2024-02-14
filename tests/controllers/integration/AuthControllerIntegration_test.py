import json
import os

import sys

# ---------- path config --------------------------------------------------------------------#
# Get the parent directory of the current directory (tests/controllers/integration)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Add the parent directory to the Python path
sys.path.append(parent_dir)
# ---------- path config --------------------------------------------------------------------#


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


# ----------------------------------------------------------------------------------------------------------------
# Log-in screen extended --> TBD ON RETURNS??

def verify_token_DNE(response):
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('token') is None or response_data.get('token') == ""

def test_001_verify_logged_out(test_client):
    data = {'username': '', 'password': ''}
    response = test_client.post('/login', json=data)
    verify_expected_error(response, 'Username or password are not provided.', 400)
    verify_token_DNE(response)

def test_002_verify_success_story(test_client):
    # waiting on return 
    assert None is None

def test_003_verify_video(test_client):
    # waiting on return
    assert None is None


# ----------------------------------------------------------------------------------------------------------------






# User 1 -> austin
def test_001_handle_signup_valid(test_client):
    data = {'username': 'austin', 'password': '@W93GW1s&0GO', 'first_name': 'austin', 'last_name': 'Holmes'}
    response = test_client.post('/signup', json=data)

    assert response.status_code == 201

    verify_token_exists(response)
    verify_login(test_client, data)


def test_002_handle_signup_duplicate_user_failed(test_client):
    data = {'username': 'austin', 'password': '54a8&9$HM@', 'first_name': 'austin', 'last_name': 'Holmes'}

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
    data = {'username': 'clifford', 'password': '?0y8~16Nfhg%', 'first_name': 'Cliff', 'last_name': 'Barnes'}
    response = test_client.post('/signup', json=data)
    assert response.status_code == 201

    verify_token_exists(response)
    verify_login(test_client, data)


# User 3 -> T-Bone
def test_006_handle_signup_valid_create_test_user3(test_client):
    data = {'username': 'T-Bone', 'password': '1oT;8Jg5J3w4', 'first_name': 'T-Bone', 'last_name': 'Steak'}
    response = test_client.post('/signup', json=data)
    assert response.status_code == 201

    verify_token_exists(response)
    verify_login(test_client, data)


# User 4 -> Cleo
def test_007_handle_signup_valid_create_test_user4(test_client):
    data = {'username': 'Cleo', 'password': '988a8&9#HM@', 'first_name': 'Cleo', 'last_name': 'Patra'}
    response = test_client.post('/signup', json=data)
    assert response.status_code == 201

    verify_token_exists(response)
    verify_login(test_client, data)


# User 5 -> Machiavelli
def test_008_handle_signup_valid_create_test_user5(test_client):
    data = {'username': 'Machiavelli', 'password': '18v3@8Q3"j|X', 'first_name': 'Machiavelli',
            'last_name': 'Donatella'}
    response = test_client.post('/signup', json=data)
    assert response.status_code == 201

    verify_token_exists(response)
    verify_login(test_client, data)


def test_009_handle_signup_max_users_reached(test_client):
    data = {'username': 'Hamburger', 'password': 'DOFp6(YF%22u', 'first_name': 'Cheese', 'last_name': 'Hamburger'}
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


# -----------------------------------------------------------------------------------------------------------#
# Job Post Testing
# Job 1-> IT Job Post
def test_001_handle_JobPost_valid(test_client):
    data = {'title': 'IT', 'desc': 'User Support', 'employer': 'USF', 'location': 'Tampa,Fl', 'salary': '50000'}
    response = test_client.post('/job_post', json=data)
    assert response.status_code == 201


def test_002_handle_job_post_Missing_Title(test_client):
    data = {'title': '', 'desc': 'Tester', 'employer': 'USF', 'location': 'Tampa,Fl', 'salary': '55000'}

    response = test_client.post('/job_post', json=data)
    verify_expected_error(response, 'Required job posting information not provided.', 400)


def test_003_handle_job_post_Missing_Desc(test_client):
    data = {'title': 'Programmer', 'desc': '', 'employer': 'Epic Games', 'location': 'Charlotte NC', 'salary': '120000'}

    response = test_client.post('/job_post', json=data)
    verify_expected_error(response, 'Required job posting information not provided.', 400)


def test_004_handle_job_post_Missing_Employer(test_client):
    data = {'title': 'Tester', 'desc': 'Make sure code it working well', 'employer': '', 'location': 'Atlanta,GA',
            'salary': '90000'}

    response = test_client.post('/job_post', json=data)
    verify_expected_error(response, 'Required job posting information not provided.', 400)


def test_005_handle_job_post_Missing_Location(test_client):
    data = {'title': 'Designer', 'desc': 'Draft Cad drawings', 'employer': 'Nvidia', 'location': '', 'salary': '130000'}

    response = test_client.post('/job_post', json=data)
    verify_expected_error(response, 'Required job posting information not provided.', 400)


def test_006_handle_job_post_Missing_Salary(test_client):
    data = {'title': 'Waiter', 'desc': 'Serve Food', 'employer': 'Cheescake Factory', 'location': 'Sarasota,Fl',
            'salary': ''}

    response = test_client.post('/job_post', json=data)
    verify_expected_error(response, 'Required job posting information not provided.', 400)


def test_006_handle_job_post_Missing_Everything(test_client):
    data = {'title': '', 'desc': '', 'employer': '', 'location': '', 'salary': ''}

    response = test_client.post('/job_post', json=data)
    verify_expected_error(response, 'Required job posting information not provided.', 400)


# Job 2-> Software Lead
def test_007_handle_JobPost_valid_2(test_client):
    data = {'title': 'Software Lead', 'desc': 'Help teammates with programming', 'employer': 'Facebook',
            'location': 'Dallas,Tx', 'salary': '80000'}
    response = test_client.post('/job_post', json=data)
    assert response.status_code == 201


def test_008_handle_JobPost_valid_3(test_client):
    data = {'title': 'Database assistant', 'desc': 'Help manage database', 'employer': 'Microsoft',
            'location': 'Houston,Tx', 'salary': '95000'}
    response = test_client.post('/job_post', json=data)

    assert response.status_code == 201


def test_009_handle_JobPost_valid_4(test_client):
    data = {'title': 'CEO', 'desc': 'Run the Business', 'employer': 'Twitter', 'location': 'California',
            'salary': '1500000'}
    response = test_client.post('/job_post', json=data)

    assert response.status_code == 201


def test_010_handle_JobPost_valid_3(test_client):
    data = {'title': 'TechnoKing', 'desc': 'Better Than CEO', 'employer': 'Tesla', 'location': 'Your mind',
            'salary': '35000000'}
    response = test_client.post('/job_post', json=data)

    assert response.status_code == 201


def test_009_handle_Max_Job_Posted_Reached(test_client):
    data = {'title': 'Manager', 'desc': 'Handle project and team development', 'employer': 'Google',
            'location': 'Silicon Valley', 'salary': '150000'}
    response = test_client.post('/job_post', json=data)
    verify_expected_error(response, 'Job posting limit reached.', 507)


# ----------------------------------------------------------------------------------------------------------------
# User Search Testing

def test_001_handle_User_Search_Invalid_Name(test_client):
    data = {'first_name': 'John', 'last_name': 'Doe'}
    response = test_client.post('/user_search', json=data)
    verify_expected_error(response, 'They are not yet a part of the InCollege system', 400)


def test_002_handle_User_Search_Invalid_First_Name(test_client):
    data = {'first_name': 'John', 'last_name': 'Holmes'}
    response = test_client.post('/user_search', json=data)
    verify_expected_error(response, 'They are not yet a part of the InCollege system', 400)


def test_003_handle_User_Search_Invalid_Last_Name(test_client):
    data = {'first_name': 'T-Bone', 'last_name': 'Doe'}
    response = test_client.post('/user_search', json=data)
    verify_expected_error(response, 'They are not yet a part of the InCollege system', 400)


def test_004_handle_User_Search_Valid_Name_1(test_client):
    data = {'first_name': 'Cliff', 'last_name': 'Barnes'}
    response = test_client.post('/user_search', json=data)
    assert response.status_code == 200


def test_005_handle_User_Search_Valid_Name_1(test_client):
    data = {'first_name': 'Machiavelli', 'last_name': 'Donatella'}
    response = test_client.post('/user_search', json=data)
    assert response.status_code == 200

