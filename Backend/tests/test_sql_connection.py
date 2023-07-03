import unittest
from unittest import mock
import mysql.connector
from ..sql_connection import SQLConnection

class TestSQLConnection(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case.

        This method is called before each test case execution.
        """

        # Patching the 'mysql.connector.connect' method using the 'mock.patch' function
        self.connection_patch = mock.patch('mysql.connector.connect')
        # Starting the patch and capturing the mocked connect method
        self.mock_connect = self.connection_patch.start()

    def tearDown(self):
        """
        Clean up the test case.

        This method is called after each test case execution.
        """

        # Stopping the patch and restoring the original behavior of 'mysql.connector.connect'
        self.connection_patch.stop()

    def test_connect(self):
        """
        Test the connect() method of SQLConnection.

        This test case verifies that the connect() method correctly establishes a connection
        with the MySQL database and assigns it to the SQLConnection object.
        """

        # Create an instance of SQLConnection
        sql_connection = SQLConnection()
        # Assert that the connection attribute is initially None
        self.assertIsNone(sql_connection.connection)

        # Create a mock connection object
        mock_connection = mock.Mock(spec=mysql.connector.MySQLConnection)
        # Configure the mock connect method to return the mock connection
        self.mock_connect.return_value = mock_connection

        # Call the connect method and capture the returned connection
        connection = sql_connection.connect()
        # Assert that the returned connection is the same as the mock connection
        self.assertEqual(connection, mock_connection)
        # Assert that the connection attribute now holds the mock connection
        self.assertEqual(sql_connection.connection, mock_connection)

    def test_close(self):
        """
        Test the close() method of SQLConnection.

        This test case verifies that the close() method correctly closes the MySQL connection
        stored in the SQLConnection object.
        """

        # Create an instance of SQLConnection
        sql_connection = SQLConnection()
        # Create a mock connection object
        mock_connection = mock.Mock(spec=mysql.connector.MySQLConnection)
        # Assign the mock connection to the connection attribute of sql_connection
        sql_connection.connection = mock_connection

        # Call the close method on sql_connection
        sql_connection.close()
        # Assert that the close method of mock_connection is called once
        mock_connection.close.assert_called_once()
        # Assert that the connection attribute of sql_connection is now None
        self.assertIsNone(sql_connection.connection)



