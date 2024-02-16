from incollege.repositories import UserRepository


def find_users_by_name(first_name, last_name):
    result = UserRepository.search_users_by_name(first_name, last_name)
    if result:
        return vars(result[0])
