from incollege.exceptions.ContentException import ContentException
from incollege.repositories import UserRepository


def search_users(first_name='', last_name='', university='', major=''):
    if not first_name and not last_name and not university and not major:
        raise ContentException('Required search parameters not provided.', 400)
    result = UserRepository.search_users(first_name, last_name, university, major)
    if not result:
        raise ContentException('No matching users found.', 404)
    return result


def update_preference(user_id, preference_name, preference_value):
    user = UserRepository.get_user(user_id)
    if not user:
        raise ContentException('No such user.', 404)
    if preference_name == "education" and len(preference_value) < 1:
        raise ContentException('Education must contain at least one value.', 409)
    if preference_name == "education" and len(preference_value) >512:
        raise ContentException('Education must not exceed 512 characters',404)
    if preference_name == "experience" and len(preference_value)>100:
        raise ContentException('Experience must not exceed 100 characters',404)
    if preference_name is None or preference_name == '' or preference_value is None or preference_value == '':
        #Since these values can be empty, will raise only when name is not any of them.
        if (preference_name == "experience") or (preference_name == "bio") or (preference_name == "major") or (preference_name == "university"):
            print(preference_name, preference_value)
        else:

            raise ContentException('Required preference parameters not provided.', 400)
    if not hasattr(user, preference_name):
        raise ContentException('No such preference.', 404)
    setattr(user, preference_name, preference_value)
    UserRepository.update_user(user)


def get_user(user_id):
    result = UserRepository.get_user(user_id)
    if not result:
        raise ContentException('No such user.', 404)
    return result
