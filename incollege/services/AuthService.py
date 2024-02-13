# Authentication Service
# Handles sign in and sign up requests at the data layer - verifies if users exists and matches password
import datetime

import jwt

import incollege.config.Config as Config
import hashlib
import re
import incollege.repositories.AuthRepository as AuthRepository
from incollege.exceptions.AuthException import AuthException


def validate_password(password):
    return bool(re.search(r'(?=.*\d)(?=.*[^A-Za-z0-9])(?=.*[A-Z])(^.{8,12}$)', password))


def hash_password(password):
    return hashlib.sha512(str.encode(password + Config.SALT)).hexdigest()


def login(username, password):
    if not username or not password:
        raise AuthException("Username or password are not provided.", 400)

    stored_hash = AuthRepository.get_password_hash(username)
    if stored_hash != hash_password(password):
        raise AuthException("Invalid username or password.")

    return create_token(username)


def signup(username, password, first_name, last_name):
    if not username or not password:
        raise AuthException("Username or password are not provided.", 400)
    if not validate_password(password):
        raise AuthException("Password does not meet requirements.", 400)
    if AuthRepository.user_exists(username):
        raise AuthException("Username already exists.", 409)
    if AuthRepository.name_exists(first_name, last_name):
        raise AuthException("User with first name and last name already exists.", 409)
    if AuthRepository.get_user_count() >= Config.USER_LIMIT:
        raise AuthException("User limit reached.", 507)

    AuthRepository.create_user(username, hash_password(password), first_name, last_name)
    return create_token(username)


def job_post(title, desc, employer, location, salary):
    if not title or not desc or not employer or not location or not salary:
        raise AuthException("Required job posting information not provided.", 400)
    if AuthRepository.get_job_count() >= Config.JOB_LIMIT:
        raise AuthException("Job posting limit reached.", 507)

    AuthRepository.create_job(title, desc, employer, location, salary)


def find_user_name(first_name, last_name):
    if AuthRepository.search_for_user(first_name, last_name):
        return "They are a part of the InCollege system"
    else:
        return "They are not yet a part of the InCollege system"


def create_token(username):
    payload = {
        'usr': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Config.TOKEN_DURATION)
    }
    return jwt.encode(payload, Config.SECRET, algorithm='HS512')


def decode_token(token):
    try:
        return jwt.decode(token, Config.SECRET, algorithms=['HS512'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
