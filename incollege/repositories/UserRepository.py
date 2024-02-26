# User Repository
# Stores and retrieves user metadata

from incollege.entity.User import User
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper('users', User, ['user_id'])


def create_user(user):
    UNIVERSAL.create_object(user)


def get_user(user_id):
    result = UNIVERSAL.get_objects({'user_id': user_id})
    if result:
        return result[0]


def search_users_by_name(first_name, last_name, university, major):
    return UNIVERSAL.get_objects({'first_name': first_name, 'last_name': last_name, 'university': university, 'major': major})


def update_user(user):
    UNIVERSAL.insert_update_object(user)

# def send_request(sender_user_id, receiver_user_id):
#     UNIVERSAL.create_connect_request(sender_user_id, receiver_user_id)
