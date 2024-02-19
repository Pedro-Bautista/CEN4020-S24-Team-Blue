# User Repository
# Stores and retrieves user metadata

from incollege.entity.User import User
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper
from incollege.repositories.DBConnector import print_users_table

UNIVERSAL = UniversalRepositoryHelper('users', User)


def create_user(user):
    UNIVERSAL.create_object(user)


def get_user(user_id):
    result = UNIVERSAL.get_objects({'user_id': user_id})
    if result:
        return result[0]


def search_users_by_name(first_name, last_name):
    return UNIVERSAL.get_objects({'first_name': first_name, 'last_name': last_name})


def update_pref(user_id, preference, state):
    
    db_column = {
        'email': 'email_pref',
        'sms': 'SMS_pref',
        'targetedAd': 'targeted_adv',
        'spanish': 'language'
    }.get(preference)

    if db_column:
        # update the preference column for the user
        UNIVERSAL.update_object({'user_id': user_id}, {db_column: 1 if state else 0})
        
    else:
        raise ValueError("Invalid preference name")