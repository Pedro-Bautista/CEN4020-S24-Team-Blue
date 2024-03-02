from incollege.exceptions.ContentException import ContentException
from incollege.repositories import ConnectionsRepository
from incollege.entity.ConnectionRequest import ConnectionRequest

import uuid

def create_connection_id():
    return str(uuid.uuid4())

def send_connection_request(sender_user_id, receiver_user_id):
    # double check the users exist? 
    conn_id = create_connection_id()
    connection_request = ConnectionRequest(conn_id, sender_user_id, receiver_user_id, 'pending')
    ConnectionsRepository.send_request(connection_request)


def get_requests_list(target_user_id):

    result = ConnectionsRepository.get_pending_requests_by_recipient_id(target_user_id)

    if not result:
        raise ContentException("Failure to retrieve connection requests.", 404)
    return result

def get_accepted_list(target_user_id):
    result = ConnectionsRepository.get_friends_by_user_id(target_user_id)
    if not result:
        raise ContentException("Fail to retrieve,no accepted connections.", 404)
    return result

def change_conn_status(requestId, status):
    change_data = {
        "request_id": requestId,
        "status": status
    }
    ConnectionsRepository.update_connection_request(change_data)