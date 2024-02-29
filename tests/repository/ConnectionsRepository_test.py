from unittest import mock, TestCase
from incollege.repositories.ConnectionsRepository import *

class ConnectionsRepositoryTest(TestCase):
    @mock.patch('incollege.repositories.ConnectionsRepository.UNIVERSAL')
    def test_change_conn_status_accepted(self, mock_universal):
        change_data = {
            'request_id': 'request_uuid',
            'status': 'accepted'
        }
        
        change_conn_status(change_data)
        
        mock_universal.updateConnection.assert_called_once_with(change_data)
        mock_universal.printTable.assert_called_once()
    
    @mock.patch('incollege.repositories.ConnectionsRepository.UNIVERSAL')
    def test_change_conn_status_rejected(self, mock_universal):
        change_data = {
            'request_id': 'request_uuid',
            'status': 'rejected'
        }
        
        change_conn_status(change_data)
        
        mock_universal.delete_entry.assert_called_once_with({'request_id': 'request_uuid'})
        mock_universal.printTable.assert_called_once()
        
class ConnectionsRepositoryTestSendRequest(TestCase):
    @mock.patch('incollege.repositories.ConnectionsRepository.UNIVERSAL')
    def test_send_request(self, mock_universal):
        request_data = {
            'sender_user_id': 'user1_uuid',
            'receiver_user_id': 'user2_uuid',
            'status': 'pending'
        }
        
        send_request(request_data)
        
        mock_universal.create_object.assert_called_once_with(request_data)

class ConnectionsRepositoryTestGetRequestsList(TestCase):
    @mock.patch('incollege.repositories.ConnectionsRepository.UNIVERSAL')
    def test_get_requests_list(self, mock_universal):
        target_user_id = 'user2_uuid'
        expected_query = {'receiver_user_id': target_user_id, 'status': 'pending'}
        
        get_requests_list(target_user_id)
        
        mock_universal.get_objects.assert_called_once_with(expected_query)

class ConnectionsRepositoryTestGetAcceptedList(TestCase):
    @mock.patch('incollege.repositories.ConnectionsRepository.UNIVERSAL')
    def test_get_accepted_list(self, mock_universal):
        target_user_id = 'user_uuid'
        expected_query_receiver = {'receiver_user_id': target_user_id, 'status': 'accepted'}
        expected_query_sender = {'sender_user_id': target_user_id, 'status': 'accepted'}
        
        get_accepted_list(target_user_id)
        
        calls = [mock.call(expected_query_receiver), mock.call(expected_query_sender)]
        mock_universal.get_objects.assert_has_calls(calls, any_order=True)