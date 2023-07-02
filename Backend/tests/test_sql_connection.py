import unittest
from unittest import mock
import sys
sys.path.append("..")
from sql_connection import SQLConnection

class SQLConnectionTest(unittest.TestCase):
    def setUp(self):
        self.sql_connection = SQLConnection()

    def tearDown(self):
        self.sql_connection.close()

    @mock.patch('sql_connection.mysql.connector.connect')
    def test_connect(self, mock_connect):
        # Mock the connect method
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection

        connection = self.sql_connection.connect(user='root', password='root', database='grocery_store')

        # Assertions
        mock_connect.assert_called_once_with(user='root', password='root', database='grocery_store')
        self.assertEqual(connection, mock_connection)


