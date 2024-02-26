from incollege.exceptions.ContentException import ContentException
from incollege.repositories import UserRepository


def find_users_by_name(first_name, last_name, university, major):
    # Using and instead of Or because we only need one parameter at a time to search.
    if not first_name and not last_name and not university and not major:
        raise ContentException('Required search parameters not provided.', 400)
    result = UserRepository.search_users_by_name(first_name, last_name, university, major)
    if not result:
        raise ContentException('No matching users found.', 404)
    return result


def update_preference(user_id, preference_name, preference_value):
    user = UserRepository.get_user(user_id)
    if not user:
        raise ContentException('No such user.', 404)
    if not preference_name or not preference_value:
        raise ContentException('Required preference parameters not provided.', 400)
    if not hasattr(user, preference_name):
        raise ContentException('No such preference.', 404)
    setattr(user, preference_name, preference_value)
    UserRepository.update_user(user)
