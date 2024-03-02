from incollege.exceptions.ContentException import ContentException
from incollege.repositories import ConnectionsRepository
from incollege.entity.ConnectionRequest import ConnectionRequest, ConnectionRequestStatus


def send_connection_request(sender_user_id, recipient_user_id):
    # TODO: double check the users exist
    connection_request = ConnectionRequest(sender_user_id, recipient_user_id, ConnectionRequestStatus.PENDING)
    ConnectionsRepository.create_connection_request(connection_request)


def get_pending_requests_by_recipient_user_id(recipient_user_id):
    result = ConnectionsRepository.get_pending_requests_by_recipient_user_id(recipient_user_id)
    if not result:
        raise ContentException("No matching connection requests found.", 404)
    return result


def get_connections_by_user_id(user_id):
    result = ConnectionsRepository.get_connections_by_user_id(user_id)
    if not result:
        raise ContentException("No matching connection requests found.", 404)
    return result


def update_connection_request(sender_user_id, recipient_user_id, status):
    connection_request = ConnectionsRepository\
        .get_requests_by_sender_and_recipient_user_id(sender_user_id, recipient_user_id)
    connection_request.status = status

    ConnectionsRepository.update_connection_request(connection_request)
