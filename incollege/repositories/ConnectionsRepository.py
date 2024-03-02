# Connections/requests repository
# handles requests to connect and accepted connection changes in the db

from incollege.entity.ConnectionRequest import ConnectionRequest, ConnectionStatus
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper("connections", ConnectionRequest, ['sender_user_id', 'recipient_user_id'])


def create_connection_request(connection_request):
    UNIVERSAL.create_object(connection_request)


def get_requests_by_sender_and_recipient_user_id(sender_user_id, recipient_user_id):
    results = UNIVERSAL.get_objects_intersection({'sender_user_id': sender_user_id,
                                                  'recipient_user_id': recipient_user_id})
    if results:
        return results[0]


def get_pending_requests_by_recipient_id(recipient_user_id):
    results = UNIVERSAL.get_objects_intersection({'recipient_user_id': recipient_user_id,
                                                  'status': ConnectionStatus.PENDING})
    return results


def get_pending_requests_by_sender_id(sender_user_id):
    results = UNIVERSAL.get_objects_intersection({'recipient_user_id': sender_user_id,
                                                  'status': ConnectionStatus.PENDING})
    return results


def get_connections_by_user_id(user_id):
    result_receiver = UNIVERSAL.get_objects_intersection({'recipient_user_id': user_id,
                                                          'status': ConnectionStatus.ACCEPTED})
    result_sender = UNIVERSAL.get_objects_intersection({'sender_user_id': user_id,
                                                        'status': ConnectionStatus.ACCEPTED})

    results = result_sender + result_receiver

    return results


def update_connection_request(mutated_connection_request):
    UNIVERSAL.insert_update_object(mutated_connection_request)
