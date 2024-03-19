# Global Database Connection Handler
# Creates global single database connection to avoid repeat connections from individual repositories

import sqlite3
from sqlite3 import Connection

import incollege.config.Config as Config

conn = None


def get_connection() -> Connection:
    """Obtains the existing database connection. If it does not exist, forms a new one and returns it.

    Returns:
        Connection: Database connection.
    """
    global conn
    if conn is None:
        conn = sqlite3.connect(Config.DATABASE_NAME, check_same_thread=False)
    return conn


def close_connection():
    """Closes any existing database connection.
    """
    if conn is not None:
        conn.close()


def create_tables():
    """Creates database tables based on schema.sql.
    """
    with open(Config.DATABASE_SCHEMA, 'r') as sql_file:
        sql_script = sql_file.read()

    get_connection().cursor().executescript(sql_script)
