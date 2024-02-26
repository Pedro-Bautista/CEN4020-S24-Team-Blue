from incollege.exceptions.ContentException import ContentException
from incollege.repositories import ConnectionsRepository
from incollege.entity.RequestConn import connectionRequest

import uuid

def create_connection_id():
    return str(uuid.uuid4())

def send_connection_request(sender_user_id, receiver_user_id):
    # double check the users exist? 
    conn_id = create_connection_id()
    connection_request = connectionRequest(conn_id, sender_user_id, receiver_user_id, 'pending')
    ConnectionsRepository.send_request(connection_request)


def get_requests_list(target_user_id):

    result = ConnectionsRepository.get_requests_list(target_user_id)

    if not result:
        raise ContentException("Failure to retrieve connection requests.", 404)
    return result