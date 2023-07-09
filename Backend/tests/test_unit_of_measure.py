import unittest
from unittest.mock import MagicMock
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Backend.unit_of_measure import get_unit_of_measure

class TestUnit_Of_Measure(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case.

        This method is called before each test case execution.
        """
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.unit_of_measures = get_unit_of_measure(self.mock_connection)

    def test_get_unit_of_measure(self):
        # Create a mock connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.__iter__.return_value = [(1, 'kg'), (2, 'lb')]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Call the get_unit_of_measure function
        unit_of_measure = get_unit_of_measure(mock_connection)

        # Assert the response is correct
        expected_response = [
            {'unit_of_measure_id': 1, 'unit_of_measure_name': 'kg'},
            {'unit_of_measure_id': 2, 'unit_of_measure_name': 'lb'}
        ]
        self.assertEqual(unit_of_measure, expected_response)

        # Assert that the cursor and execute methods were called
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT unit_of_measure_id, unit_of_measure_name FROM unit_of_measure")
