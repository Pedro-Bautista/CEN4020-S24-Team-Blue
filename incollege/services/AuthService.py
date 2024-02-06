# Authentication Service
# Handles sign in and sign up requests at the data layer - verifies if users exists and matches password
import datetime

import jwt

import incollege.config.Config as Config
import hashlib
import re
import incollege.repositories.AuthRepository as AuthRepository

# This should ideally be on the user interface end, but that does not exist, so it's here
def validate_password(password):
    length_check = 8 <= len(password) <= 12
    types_check = bool(re.search(r'(?=.*\d)(?=.*[^A-Za-z0-9])(?=.*[A-Z])', password))
    return length_check and types_check

def hash_password(password):
    return hashlib.sha512(str.encode(password+Config.SALT)).digest()

def login(username, password):
    try:
        if not username or not password:
            raise ValueError("Username or password are not provided")

        stored_hash = AuthRepository.get_password_hash(username)
        if stored_hash == hash_password(password):
            return (True, create_token(username))
        raise ValueError("Invalid username or password")
    except Exception as e:
        print(f"Login failed: {e}")
        return (False, str(e))

def signup(username, password) -> (bool, str) :
    try:
        if not username or not password:
            raise ValueError("Username or password are not provided")
          
        if not validate_password(password):
            raise ValueError("Password does not meet requirements")

        if AuthRepository.user_exists(username):
            raise ValueError("Username already exists")

        if AuthRepository.get_user_count() >= Config.USER_LIMIT:
            raise ValueError("User limit reached")

        AuthRepository.create_user(username, hash_password(password))
        return (True, create_token(username))
    except Exception as e:
        print(f"Signup failed: {e}")
        return (False, str(e))
    
def create_token(username):
    payload = {
        'usr': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Config.TOKEN_DURATION)
    }
    return jwt.encode(payload, Config.SECRET, algorithm='HS512')

def decode_token(token):
    try:
        return jwt.decode(token, Config.SECRET, algorithms=['HS512'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as error:
        return None
