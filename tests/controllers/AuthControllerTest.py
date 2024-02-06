import sqlite3
import unittest
import os

from unittest.mock import patch

from incollege.repositories.DBConnector import *
import incollege.controllers.AuthController as Auth

class TestSuiteName(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Attempting to reset database')
        try:
            os.remove(Config.DATABASE_NAME)
            print('Successfully deleted test database')
        except FileNotFoundError:
            print('File does not exist... No need to reset')

        create_tables()

    def test_user_does_not_exist(self):
        test_login = Auth.login('austin', '1234')
        assert test_login is None

    def test_user_does_not_exist_2(self):
        create_user = Auth.signup('austin', '54a8&9$HM@')
        test_login = Auth.login('austin', '54a8&9$HM@')
        assert test_login is not None

    @classmethod
    def tearDownClass(cls):
        close_connection()
