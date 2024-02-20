from incollege.exceptions.ContentException import ContentException
from incollege.repositories import UserRepository


def find_users_by_name(first_name, last_name):
    result = UserRepository.search_users_by_name(first_name, last_name)
    if result:
        return vars(result[0])


def update_preference(user_id, preference_name, preference_value):
    user = UserRepository.get_user(user_id)
    if not user:
        raise ContentException("No such user.", 404)
    if not hasattr(user, preference_name):
        raise ContentException("No such preference.", 404)
    setattr(user, preference_name, preference_value)
    UserRepository.update_user(user)
    