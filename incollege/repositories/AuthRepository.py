# Authentication Repository
# Stores and retrieves existing user and password data

from incollege.repositories.DBConnector import get_connection


def get_user_count():
    cursor = get_connection().cursor()
    result = cursor.execute('''
        SELECT COUNT (*) FROM auth
    ''').fetchone()
    return result[0]


def get_password_hash(username):
    cursor = get_connection().cursor()
    result = cursor.execute('''
        SELECT password_hash FROM auth WHERE username = (?)
    ''', (username,)).fetchone()
    if result:
        return result[0]


def user_exists(username):
    cursor = get_connection().cursor()
    result = cursor.execute('''
        SELECT COUNT (*) FROM auth WHERE username = (?)
    ''', (username,)).fetchone()
    return result is not 0


def create_user(username, password_hash):
    cursor = get_connection().cursor()
    cursor.execute('''
        INSERT INTO auth (username, password_hash) VALUES (?,?)
    ''', (username, password_hash,))
    get_connection().commit()


def delete_user(username):
    cursor = get_connection().cursor()
    cursor.execute('''
        DELETE FROM auth WHERE username = ?
    ''', (username,))
    get_connection().commit()
