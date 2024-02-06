import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import pytest
from flask import Flask
from incollege.controllers.AuthController import configure_auth_routes
from incollege.repositories.DBConnector import create_tables

"""
signup with valid user and pass
signup with repeat username
signup with repeat pass
signup with empty user
signup with empty pass
signup with invalid pass (too long)
signup with invalid pass (no num, no special letter)
signup 5 additional users (should return error at 5th user)

login with invalid user 
login with invalid pass
login with empty user
login with empty pass
login with valid user and pass

call Home
call Jobs
call People
call Learn
call Profile
call Logout
"""

@pytest.fixture
def app():
    # Create a Flask application
    app = Flask(__name__)

    # Configure authentication routes
    configure_auth_routes(app)

    # Create tables in the database
    create_tables()

    yield app


@pytest.fixture
def client(app):
    # Create a test client using the Flask application
    with app.test_client() as client:
        yield client


def test_signup(client):
    # Create JSON data for signup request
    signup_data = {'username': 'student1', 'password': 'sp3ci@L8'}

    # Make a POST request to the signup route with signup data
    response = client.post('/signup', json=signup_data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the response contains a token
    assert 'token' in json.loads(response.data)


def test_login(client):
    # Create JSON data for login request
    login_data = {'username': 'student1', 'password': 'sp3ci@L8'}

    # Make a POST request to the login route with login data
    response = client.post('/login', json=login_data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the response contains a token
    assert 'token' in json.loads(response.data)


def test_login_invalid(client):

    login_data = {'username': 'student1', 'password': 'sp3ci@L9'}

    response = client.post('/login', json=login_data)

    # Check if the response status code is internal error (Unauthorized)
    assert response.status_code == 500