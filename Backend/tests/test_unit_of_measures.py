import unittest
from unittest.mock import MagicMock
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Backend.unit_of_measures import UnitOfMeasures

""" \test @ref R71_0"""
class Unit_Of_MeasuresTestCase(unittest.TestCase):
    """ \test @ref R71_0"""
    def setUp(self):
        """
        Set up the test case by creating mock objects and initializing the 'unit_of_measure' instance.
        """
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.unit_of_measures = UnitOfMeasures(self.mock_connection)

    """ \test @ref R71_0"""
    def test_get_unit_of_measures(self):
        """
        Test case for the 'get_unit_of_measure' method of the 'unit_of_measure' class.
        """

        # Mock the result set returned by the query
        mock_result_set = [
            (1, 'kg'),
            (2, 'lbs')
        ]
        self.mock_cursor.__iter__.return_value = iter(mock_result_set)

        # Call the method under test
        result = self.unit_of_measures.get_unit_of_measures()

        # Assert the expected SQL query was executed
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM unit_of_measures")

        # Assert the expected response was returned
        expected_response = [
            {'unit_of_measure_id': 1, 'unit_of_measure_name': 'kg'},
            {'unit_of_measure_id': 2, 'unit_of_measure_name': 'lbs'}
        ]
        self.assertEqual(result, expected_response)
