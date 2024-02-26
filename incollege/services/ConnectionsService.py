from incollege.exceptions.ContentException import ContentException
from incollege.repositories import ConnectionsRepository

def send_connection_request(sender_user_id, receiver_user_id):
    # double check the users exist? 
    result = ConnectionsRepository.send_request(sender_user_id, receiver_user_id)

    if not result:
        raise ContentException("Request Failed to Send.", 404)

