import json
from unittest import mock
import pytest
from flask import Flask

from incollege.controllers.ControllerAdvice import configure_controller_advice
from incollege.controllers.JobController import *
from incollege.entity.AuthJWT import AuthJWT
from incollege.entity.Job import Job
from incollege.exceptions.ContentException import ContentException


test_job = Job('some_job_id', 'some_owner_user_id', 'some_title', 'some_desc', 'some_employer',
               'some_location', 123456)
test_invalid_job = Job('some_job_id', 'some_owner_user_id', '', 'some_desc', 'some_employer',
                       'some_location', 123456)
test_job_data = vars(test_job)
test_invalid_job_data = vars(test_invalid_job)
test_jwt_header = {'token': AuthJWT('some_user_id', 'user').encode}
test_invalid_jwt_header = {'token': 'invalid_token'}


@pytest.fixture(scope='module')
def test_client():
    test_app = Flask(__name__)
    test_app.config['TESTING'] = True
    configure_job_routes(test_app)
    configure_controller_advice(test_app)

    with test_app.test_client() as test_client:
        with test_app.app_context():
            yield test_client


@mock.patch('incollege.services.JobService.post_job')
def test_handle_job_post_success(mock_post_job, test_client):
    data = test_job_data
    response = test_client.post('/job_post', json=data, headers=test_jwt_header)

    assert response.status_code == 201


@mock.patch('incollege.services.JobService.post_job')
def test_handle_job_post_no_token(mock_post_job, test_client):
    data = test_job_data
    response = test_client.post('/job_post', json=data, headers=None)

    assert response.status_code == 401
    assert get_response_error_desc(response) == 'Authentication token missing.'


@mock.patch('incollege.services.JobService.post_job')
def test_handle_job_post_unauthorized(mock_post_job, test_client):
    data = test_job_data
    response = test_client.post('/job_post', json=data, headers=test_invalid_jwt_header)

    assert response.status_code == 401
    assert get_response_error_desc(response) == 'Authentication failed.'


@mock.patch('incollege.services.JobService.post_job',
            side_effect=ContentException('Required job posting information not provided.', 400))
def test_handle_job_post_malformed(mock_post_job, test_client):
    data = test_invalid_job_data
    response = test_client.post('/job_post', json=data, headers=test_jwt_header)

    assert response.status_code == 400
    assert get_response_error_desc(response) == 'Required job posting information not provided.'


def get_response_error_desc(response):
    return json.loads(response.data)['error']['description']
