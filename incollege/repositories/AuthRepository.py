# Authentication Repository
# Stores and retrieves existing user and password data

from incollege.repositories.DBConnector import get_connection


def get_user_count():
    cursor = get_connection().cursor()
    result = cursor.execute('''
        SELECT COUNT (*) FROM auth
    ''').fetchone()
    return result[0]

def get_job_count():
    cursor = get_connection().cursor()
    result = cursor.execute('''
        SELECT COUNT (*) FROM jobs
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
        SELECT COUNT (*) FROM auth WHERE username = (?) LIMIT 1
    ''', (username,)).fetchone()
    return result[0] >= 1

def name_exists(first_name, last_name):
    cursor = get_connection().cursor()
    result = cursor.execute('''
        SELECT COUNT (*) FROM auth WHERE first_name = (?) AND last_name = (?) LIMIT 1
    ''', (first_name, last_name)).fetchone()
    return result[0] >= 1

def create_user(username, password_hash, first_name, last_name):
    cursor = get_connection().cursor()
    cursor.execute('''
        INSERT INTO auth (username, password_hash, first_name, last_name) VALUES (?,?,?,?)
    ''', (username, password_hash, first_name, last_name,))
    get_connection().commit()
    
def create_job(title, desc, employer, location, salary):
    cursor = get_connection().cursor()
    cursor.execute('''
        INSERT INTO jobs (title, desc, employer, location, salary) VALUES (?,?,?,?,?)
    ''', (title, desc, employer, location, salary,))
    get_connection().commit()
    


def delete_user(username):
    cursor = get_connection().cursor()
    cursor.execute('''
        DELETE FROM auth WHERE username = ?
    ''', (username,))
    get_connection().commit()
