# User Repository
# Stores and retrieves user metadata

from incollege.entity.User import User
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper('users', User, ['user_id'])


def create_user(user):
    UNIVERSAL.create_object(user)


def get_user(user_id):
    result = UNIVERSAL.get_objects_intersection({'user_id': user_id})
    if result:
        return result[0]


def search_users(first_name, last_name, university, major):
    return UNIVERSAL.get_objects_fuzzy({'first_name': first_name, 'last_name': last_name,
                                        'university': university, 'major': major})


def update_user(mutated_user):
    UNIVERSAL.insert_update_object(mutated_user)
