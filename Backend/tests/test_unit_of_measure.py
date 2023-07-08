import unittest
from unittest.mock import MagicMock
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Backend.unit_of_measure import get_uoms
class TestUOMs(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case.

        This method is called before each test case execution.
        """
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.products = get_uoms(self.mock_connection)

    def test_get_uoms(self):
        # Create a mock connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.__iter__.return_value = [(1, 'kg'), (2, 'lb')]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Call the get_uoms function
        uoms = get_uoms(mock_connection)

        # Assert the response is correct
        expected_response = [
            {'uom_id': 1, 'uom_name': 'kg'},
            {'uom_id': 2, 'uom_name': 'lb'}
        ]
        self.assertEqual(uoms, expected_response)

        # Assert that the cursor and execute methods were called
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT uom_id, uom_name FROM uom")