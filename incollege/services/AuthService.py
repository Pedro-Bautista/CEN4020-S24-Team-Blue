# Authentication Service
# Handles sign in and sign up requests at the data layer - verifies if users exists and matches password

import incollege.config.Config as Config
import hashlib
import incollege.repositories.AuthRepository as AuthRepository

def hash_password(password):
    return hashlib.sha512(str.encode(password+Config.SALT)).digest()

def login(username, password):
    if not username or not password:
        return False
    stored_hash = AuthRepository.get_password_hash(username)
    return stored_hash == hash_password(password)

def signup(username, password):
    if not username or not password or AuthRepository.user_exists(username) \
            or AuthRepository.get_user_count() >= Config.USER_LIMIT:
        return False
    AuthRepository.create_user(username, hash_password(password))
    return True
