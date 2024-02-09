from unittest import mock, TestCase

from incollege.repositories.AuthRepository import *

class AuthRepositoryTest(TestCase):

    @mock.patch('incollege.repositories.AuthRepository.get_connection')
    def test_get_user_count(self, mock_get_connection):
        mock_cursor = mock_get_connection.return_value.cursor.return_value
        mock_cursor.execute.return_value.fetchone.return_value = (3, )

        result = get_user_count()

        self.assertEquals(result, 3)

    @mock.patch('incollege.repositories.AuthRepository.get_connection')
    def test_get_user_count(self, mock_get_connection):
        mock_cursor = mock_get_connection.return_value.cursor.return_value
        mock_cursor.execute.return_value.fetchone.return_value = ('some_hash', )

        result = get_password_hash('austin')

        self.assertEquals(result, 'some_hash')

    @mock.patch('incollege.repositories.AuthRepository.get_connection')
    def test_user_exists_true(self, mock_get_connection):
        mock_cursor = mock_get_connection.return_value.cursor.return_value
        mock_cursor.execute.return_value.fetchone.return_value = 1

        result = user_exists('austin')

        self.assertEquals(result, True)

    @mock.patch('incollege.repositories.AuthRepository.get_connection')
    def test_user_exists_false(self, mock_get_connection):
        mock_cursor = mock_get_connection.return_value.cursor.return_value
        mock_cursor.execute.return_value.fetchone.return_value = 0

        result = user_exists('austin')

        self.assertEquals(result, False)

    @mock.patch('incollege.repositories.AuthRepository.get_connection')
    def test_user_exists_false(self, mock_get_connection):
        mock_cursor = mock_get_connection.return_value.cursor.return_value

        create_user('austin', 'some_hash')

    @mock.patch('incollege.repositories.AuthRepository.get_connection')
    def test_user_exists_false(self, mock_get_connection):
        mock_cursor = mock_get_connection.return_value.cursor.return_value

        delete_user('austin')
