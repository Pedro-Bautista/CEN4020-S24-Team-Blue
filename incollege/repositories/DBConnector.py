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
    conn.close()


def create_tables():
    cursor = get_connection().cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auth (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            password_hash TEXT,
            permissions_group TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT
            language TEXT,
            email_pref INT,
            SMS_pref INT, 
            targeted_adv INT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            connections_index_id TEXT PRIMARY KEY,
            user_id TEXT,
            connection_id TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            title TEXT,
            desc TEXT, 
            employer TEXT,
            location TEXT, 
            salary REAL
        )
    ''')
    
    conn.commit()

