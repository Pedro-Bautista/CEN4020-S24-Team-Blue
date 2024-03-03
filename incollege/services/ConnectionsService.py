from incollege.entity.enum.ConnectionRequestStatus import ConnectionRequestStatus
from incollege.exceptions.ContentException import ContentException
from incollege.repositories import ConnectionsRepository, UserRepository
from incollege.entity.ConnectionRequest import ConnectionRequest


def send_connection_request(sender_user_id, recipient_user_id):
    if not UserRepository.get_user(sender_user_id):
        raise ContentException('No such sending user.', 404)
    if not UserRepository.get_user(recipient_user_id):
        raise ContentException('No such receiving user.', 404)
    if ConnectionsRepository.get_request_by_sender_and_recipient_user_id(sender_user_id, recipient_user_id):
        raise ContentException('Connection request already exists.', 409)
    existing_reverse_connection_request = ConnectionsRepository.get_request_by_sender_and_recipient_user_id(
        recipient_user_id, sender_user_id)
    if existing_reverse_connection_request:
        existing_reverse_connection_request.status = ConnectionRequestStatus.ACCEPTED
        ConnectionsRepository.update_connection_request(existing_reverse_connection_request)
    else:
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
        .get_request_by_sender_and_recipient_user_id(sender_user_id, recipient_user_id)
    if not connection_request:
        raise ContentException('No such connection request.', 404)
    connection_request.status = ConnectionRequestStatus().from_string(status)

    ConnectionsRepository.update_connection_request(connection_request)
