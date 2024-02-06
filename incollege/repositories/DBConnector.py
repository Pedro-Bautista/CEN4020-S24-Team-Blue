# Global Database Connection Handler
# Creates global single database connection to avoid repeat connections from individual repositories

import sqlite3
import incollege.config.Config as Config

conn = None

def get_connection():
    global conn
    if conn is None:
        conn = sqlite3.connect(Config.DATABASE_NAME)
    return conn

def close_connection():
    conn.close()

def create_tables():
    cursor = get_connection().cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auth (
            username TEXT,
            password_hash TEXT
        )
    ''')
    conn.commit()
