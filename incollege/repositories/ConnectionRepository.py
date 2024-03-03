# Connections/requests repository
# handles requests to connect and accepted connection changes in the db

from incollege.entity.ConnectionRequest import ConnectionRequest, ConnectionRequestStatus
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper("connections", ConnectionRequest, ['sender_user_id', 'recipient_user_id'])


def create_connection_request(connection_request):
    UNIVERSAL.create_object(connection_request)


def get_request_by_sender_and_recipient_user_id(sender_user_id, recipient_user_id):
    result = UNIVERSAL.get_objects_intersection({'sender_user_id': sender_user_id,
                                                 'recipient_user_id': recipient_user_id})
    if result:
        return result[0]


def get_pending_requests_by_recipient_user_id(recipient_user_id):
    result = UNIVERSAL.get_objects_intersection({'recipient_user_id': recipient_user_id,
                                                 'status': ConnectionRequestStatus.PENDING})
    if result:
        return result


def get_pending_requests_by_sender_user_id(sender_user_id):
    result = UNIVERSAL.get_objects_intersection({'sender_user_id': sender_user_id,
                                                 'status': ConnectionRequestStatus.PENDING})
    if result:
        return result


def get_connections_by_user_id(user_id):
    result_sender = UNIVERSAL.get_objects_intersection({'sender_user_id': user_id,
                                                        'status': ConnectionRequestStatus.ACCEPTED})
    result_recipient = UNIVERSAL.get_objects_intersection({'recipient_user_id': user_id,
                                                           'status': ConnectionRequestStatus.ACCEPTED})

    results = result_sender + result_recipient

    if results:
        return results


def update_connection_request(mutated_connection_request):
    UNIVERSAL.insert_update_object(mutated_connection_request)
