# User Repository
# Stores and retrieves user metadata

from incollege.entity.User import User
from incollege.entity.enum.ConnectionRequestStatus import ConnectionRequestStatus
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper('users', User, ['user_id'])


def create_user(user):
    UNIVERSAL.create_object(user)


def get_user(user_id):
    result = UNIVERSAL.get_objects_intersection({'user_id': user_id})
    if result:
        return result


def get_connection_users_by_user_id(user_id):
    query = f'''
        SELECT u.* FROM connections c INNER JOIN users u on c.recipient_user_id = u.user_id 
        OR c.sender_user_id = u.user_id WHERE (c.sender_user_id = (?) OR c.recipient_user_id = (?)) 
        AND (u.user_id != (?)) AND (c.status = {ConnectionRequestStatus.ACCEPTED})
    '''
    result = UNIVERSAL.call_sql_query(query, [user_id, user_id, user_id], True)
    if result:
        return result


def search_users(first_name, last_name, university, major):
    return UNIVERSAL.get_objects_fuzzy({'first_name': first_name, 'last_name': last_name,
                                        'university': university, 'major': major})


def update_user(mutated_user):
    UNIVERSAL.insert_update_object(mutated_user)
