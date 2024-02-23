# Global Database Connection Handler
# Creates global single database connection to avoid repeat connections from individual repositories

import sqlite3
import incollege.config.Config as Config

conn = None


def get_connection():
    global conn
    if conn is None:
        conn = sqlite3.connect(Config.DATABASE_NAME, check_same_thread=False)
    return conn


def close_connection():
    if conn is not None:
        conn.close()


def create_tables():
    with open(Config.DATABASE_SCHEMA, 'r') as sql_file:
        sql_script = sql_file.read()

    get_connection().cursor().executescript(sql_script)
