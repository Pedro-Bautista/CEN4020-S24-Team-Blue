from incollege.repositories import UserRepository


def find_users_by_name(first_name, last_name):
    result = UserRepository.search_users_by_name(first_name, last_name)
    if result:
        return vars(result[0])


def update_preferences(user_id, preference, on):
    
    try:
        UserRepository.update_pref(user_id, preference, on)
        return {'message': f'{preference} preference updated successfully'}
    except ValueError as e:
        return {'error': str(e)}
    
    