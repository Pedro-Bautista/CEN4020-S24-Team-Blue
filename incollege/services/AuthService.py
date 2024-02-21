# Authentication Service
# Handles sign in and sign up requests at the data layer - verifies if users exists and matches password
import datetime
import uuid

import jwt

import incollege.config.Config as Config
import hashlib
import re
import incollege.repositories.AuthRepository as AuthRepository
import incollege.repositories.JobRepository
import incollege.repositories.UserRepository
from incollege.entity.AuthUser import AuthUser
from incollege.entity.User import User
from incollege.exceptions.AuthException import AuthException
from incollege.repositories import UserRepository


def validate_password(password):
    return bool(re.search(r'(?=.*\d)(?=.*[^A-Za-z0-9])(?=.*[A-Z])(^.{8,12}$)', password))


def hash_password(password):
    return hashlib.sha512(str.encode(password + Config.SALT), usedforsecurity=True).hexdigest()


def create_user_id():
    return str(uuid.uuid4())


def login(username, password):
    if not username or not password:
        raise AuthException("Username or password are not provided.", 400)

    user_id = AuthRepository.get_user_id(username)
    if not user_id:
        raise AuthException("Invalid username or password.")
    stored_hash = AuthRepository.get_password_hash(user_id)
    if stored_hash != hash_password(password):
        raise AuthException("Invalid username or password.")

    permissions_group = AuthRepository.get_permissions_group(user_id)
    return create_token(user_id, permissions_group)


def signup(username, password, first_name, last_name):
    if not username or not password:
        raise AuthException("Username or password are not provided.", 400)
    if not first_name or not last_name:
        raise AuthException("First or last name are not provided", 400)
    if not validate_password(password):
        raise AuthException("Password does not meet requirements.", 400)
    if AuthRepository.get_user_id(username):
        raise AuthException("Username already exists.", 409)
    if AuthRepository.get_auth_user_count() >= Config.USER_LIMIT:
        raise AuthException("User limit reached.", 507)

    user_id = create_user_id()

    auth_user = AuthUser(user_id, username, hash_password(password), 'users')
    AuthRepository.create_auth_user(auth_user)

    user = User(user_id, username, first_name, last_name)
    UserRepository.create_user(user)

    return create_token(user_id, 'users')


def create_token(user_id, permissions_group):
    payload = {
        'usr': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Config.TOKEN_DURATION),
        'grp': permissions_group
    }
    return jwt.encode(payload, Config.SECRET, algorithm='HS512')


def decode_token(token):
    try:
        return jwt.decode(token, Config.SECRET, algorithms=['HS512'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
