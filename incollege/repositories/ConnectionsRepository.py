# Connections/requests repository
# handles requests to connect and accepted connection changes in the db

from incollege.entity.RequestConn import connectionRequest
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper("connections", connectionRequest, ["request_id"])

def send_request(request_data):
    UNIVERSAL.create_object(request_data)
   

def get_requests_list(target_user_id):
    results = UNIVERSAL.get_objects({'receiver_user_id': target_user_id, 'status': 'pending'})
    return results
def get_accepted_list(target_user_id):
    results = UNIVERSAL.get_objects({'receiver_user_id':target_user_id, 'status': 'accepted'})
    return results
    
def change_conn_status(change_data):

    requestID = change_data.get('request_id')

    if change_data.get('status') == 'accepted':
        # if changing status to accepted
        # connection = UNIVERSAL.get_objects({'request_id': requestID})
        # if connection:
        #     mutated = connection[0]
        #     mutated.status = change_data.get('status')
        #     UNIVERSAL.insert_update_object(mutated)

        UNIVERSAL.updateConnection(change_data)

        print("INSERTED THE UPDATE")

    elif change_data.get('status') == 'rejected':
        # if removing bc rejected
        keys = {'request_id': requestID}
        UNIVERSAL.delete_entry(keys)
    
    print("REQUEST ID CHANGED:::::::::::: ", requestID)
    UNIVERSAL.printTable()

