# User Repository
# Stores and retrieves user metadata

from incollege.entity.User import User
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper('users', User)


def create_user(user):
    UNIVERSAL.create_object(user)


def get_user(user_id):
    result = UNIVERSAL.get_objects({'user_id': user_id})
    if result:
        return result[0]


def search_users_by_name(first_name, last_name):
    return UNIVERSAL.get_objects({'first_name': first_name, 'last_name': last_name})
