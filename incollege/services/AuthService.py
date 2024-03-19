# Authentication Service
# Handles sign in and sign up requests at the data layer - verifies if users exists and matches password
import datetime
import uuid

import jwt

import incollege.config.Config as Config
import hashlib
import re
import incollege.repositories.AuthRepository as AuthRepository
from incollege.entity.AuthJWT import AuthJWT
from incollege.entity.AuthUser import AuthUser
from incollege.entity.User import User
from incollege.entity.enum.PermissionsGroup import PermissionsGroup
from incollege.exceptions.AuthException import AuthException
from incollege.repositories import UserRepository


def validate_password(password: str) -> bool:
    """Validates whether the password meets the requirements specified.

    The following criteria will be evaluated:
    - Must be between 8-12 characters (inclusive)
    - Must contain at least one capital letter.
    - Must contain at least one special (non-alphanumeric) character.

    Args:
        password (str): The password to be validated.

    Returns:
        bool: True if the requirements are met, False if not.
    """
    return bool(re.search(r'(?=.*\d)(?=.*[^A-Za-z0-9])(?=.*[A-Z])(^.{8,12}$)', password))


def hash_password(password: str) -> str:
    """Returns the SHA-512 hash of the input password with the :class:`~Config`-specified salt appended.

    Args:
        password (str): The password to be hashed

    Returns:
        str: The hashed password.
    """
    return hashlib.sha512(str.encode(password + Config.SALT), usedforsecurity=True).hexdigest()


def create_user_id() -> str:
    """Generates a UUID to be used as a unique identifier.

    Returns:
        str: The UUID.
    """
    return str(uuid.uuid4())


def login(username: str, password: str) -> str:
    """Executes the service-level of the login process.

    Args:
        username: The username to log in as.
        password: The password for the username.

    Returns:
        str: An encoded authentication token for the user referenced by the username.

    Raises:
        AuthException: If there is a failure to match the password to the username, or if the arguments are invalid.
    """
    if not username or not password:
        raise AuthException("Username or password are not provided.", 400)

    user_id = AuthRepository.get_user_id(username)
    if not user_id:
        raise AuthException("Invalid username or password.")
    stored_hash = AuthRepository.get_password_hash(user_id)
    if stored_hash != hash_password(password):
        raise AuthException("Invalid username or password.")

    permissions_group = AuthRepository.get_permissions_group(user_id)
    return AuthJWT(user_id, permissions_group).encode()


def signup(username: str, password: str, first_name: str, last_name: str) -> str:
    """Executes the service level of the signup process.

    Args:
        username (str): Username to sign up.
        password (str): Password to link to username.
        first_name (str): First name for profile.
        last_name (str): Last name for profile.

    Returns:
        str: An encoded authentication token for the user referenced by the username.

    Raises:
        AuthException: If the arguments are invalid, or the username already exists, or the internal user limit has \
        been reached.
    """
    if not username or not password:
        raise AuthException("Username or password are not provided.", 400)
    if not first_name or not last_name:
        raise AuthException("First or last name are not provided.", 400)
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

    return AuthJWT(user_id, PermissionsGroup.USER).encode()
