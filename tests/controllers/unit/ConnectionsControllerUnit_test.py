import json
from unittest import mock
import pytest
from flask import Flask

from incollege.controllers.ConnectionsController import configure_connection_routes
from incollege.controllers.ControllerAdvice import configure_controller_advice
from incollege.services import AuthService

test_jwt_header = {'token': AuthService.create_token('some_user_id', 'user')}
test_invalid_jwt_header = {'token': 'invalid_token'}

@pytest.fixture(scope='module')
def test_client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    configure_connection_routes(app)
    configure_controller_advice(app)

    with app.test_client() as client:
        with app.app_context():
            yield client

def get_response_error_desc(response):
    return json.loads(response.data)['error']['description']

def get_response_message(response):
    return json.loads(response.data)['message']

@mock.patch('incollege.services.ConnectionsService.send_connection_request')
def test_send_connection_request_success(mock_send_request, test_client):
    receiver_userID = 'receiver_user_id'
    response = test_client.post('/send_request', json={'receiver_userID': receiver_userID}, headers=test_jwt_header)
    
    assert response.status_code == 200
    mock_send_request.assert_called_once_with('some_user_id', receiver_userID)

@mock.patch('incollege.services.ConnectionsService.get_requests_list', return_value=[])
def test_get_requests_list_success(mock_get_requests, test_client):
    response = test_client.post('/get_requests_list', headers=test_jwt_header)
    
    assert response.status_code == 200
    assert get_response_message(response) == []
    mock_get_requests.assert_called_once_with('some_user_id')

@mock.patch('incollege.services.ConnectionsService.get_accepted_list', return_value=[])
def test_get_accepted_list_success(mock_get_accepted, test_client):
    response = test_client.post('/get_accepted_list', headers=test_jwt_header)
    
    assert response.status_code == 200
    assert get_response_message(response) == []
    mock_get_accepted.assert_called_once_with('some_user_id')

@mock.patch('incollege.services.ConnectionsService.change_conn_status')
def test_handle_conn_status_change_success(mock_change_status, test_client):
    request_id = 'request_id'
    status = 'accepted'
    response = test_client.post('/change_conn_status', json={'request_id': request_id, 'status': status}, headers=test_jwt_header)
    
    assert response.status_code == 200
    mock_change_status.assert_called_once_with(request_id, status)

@mock.patch('incollege.services.ConnectionsService.send_connection_request')
def test_send_connection_request_unauthorized(mock_send_request, test_client):
    receiver_userID = 'receiver_user_id'
    response = test_client.post('/send_request', json={'receiver_userID': receiver_userID}, headers=test_invalid_jwt_header)
    
    assert response.status_code == 401
