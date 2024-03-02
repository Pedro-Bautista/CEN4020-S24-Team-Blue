import json
from unittest import mock
import pytest
from flask import Flask

from incollege.controllers.ConnectionsController import configure_connection_routes
from incollege.controllers.ControllerAdvice import configure_controller_advice
from incollege.entity.AuthJWT import AuthJWT
from incollege.services import AuthService

test_jwt_header = {'token': AuthJWT('some_user_id', 'user').encode()}
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


@mock.patch('incollege.services.ConnectionsService.get_pending_requests_by_recipient_user_id',
            return_value=[])
def test_get_pending_requests_by_recipient_user_id_success(mock_get_pending_requests_by_recipient_user_id,
                                                           test_client):
    response = test_client.post('/get_requests_list', headers=test_jwt_header)

    assert response.status_code == 200
    assert get_response_message(response) == []
    mock_get_pending_requests_by_recipient_user_id.assert_called_once_with('some_user_id')


@mock.patch('incollege.services.ConnectionsService.get_connections_by_user_id', return_value=[])
def test_get_accepted_list_success(mock_get_connections_by_user_id, test_client):
    response = test_client.post('/get_accepted_list', headers=test_jwt_header)

    assert response.status_code == 200
    assert get_response_message(response) == []
    mock_get_connections_by_user_id.assert_called_once_with('some_user_id')


@mock.patch('incollege.services.ConnectionsService.update_connection_request')
def test_handle_conn_status_change_success(mock_update_connection_request, test_client):
    sender_id = 'sender_id'
    status = 'accepted'
    response = test_client.post('/change_conn_status', json={'sender_user_id': sender_id, 'status': status},
                                headers=test_jwt_header)

    assert response.status_code == 200
    mock_update_connection_request.assert_called_once_with(sender_id, 'some_user_id', status)


@mock.patch('incollege.services.ConnectionsService.send_connection_request')
def test_send_connection_request_unauthorized(mock_send_request, test_client):
    receiver_userID = 'receiver_user_id'
    response = test_client.post('/send_request', json={'receiver_userID': receiver_userID},
                                headers=test_invalid_jwt_header)

    assert response.status_code == 401
