# Connections/requests repository
# handles requests to connect and accepted connection changes in the db

from incollege.entity.RequestConn import connectionRequest
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper("connection_requests", connectionRequest, ["request_id"])

def send_request(request_data):
    UNIVERSAL.create_object(request_data)
    UNIVERSAL.printTable()
   

def get_requests_list(target_user_id):
    UNIVERSAL.printTable()
    print("TARGET PERSON: ", target_user_id)
    results = UNIVERSAL.get_objects({'receiver_user_id': target_user_id})
    print("RESULTS HERE: ", results)
    return results
    