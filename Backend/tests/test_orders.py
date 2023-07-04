import unittest
from unittest.mock import MagicMock, call
from datetime import datetime
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Backend.orders import Orders

class OrdersTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by creating mock objects and initializing the 'Orders' instance.
        """

        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.orders = Orders(self.mock_connection)

    def test_get_all_orders(self):
        """
        Test case for the 'get_all_orders' method of the 'Orders' class.
        """

        # Mock the result set returned by the query
        mock_result_set = [
            (1, 'John Doe', 100.0, datetime.now()),
            (2, 'Jane Smith', 200.0, datetime.now())
        ]
        self.mock_cursor.__iter__.return_value = iter(mock_result_set)

        # Call the method under test
        result = self.orders.get_all_orders()

        # Assert the expected SQL query was executed
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM orders")

        # Assert the expected response was returned
        expected_response = [
            {'order_id': 1, 'customer_name': 'John Doe', 'total_amount': 100.0, 'datetime': mock_result_set[0][3]},
            {'order_id': 2, 'customer_name': 'Jane Smith', 'total_amount': 200.0, 'datetime': mock_result_set[1][3]}
        ]
        self.assertEqual(result, expected_response)

    def test_insert_new_order(self):
        """
        Test case for the 'insert_new_order' method of the 'Orders' class.
        """

        # Mock the return value of cursor.lastrowid
        self.mock_cursor.lastrowid = 1

        # Define the test order data
        test_order = {
            'customer_name': 'John Doe',
            'total_amount': 100.0,
            'order_details': [
                {'product_id': '123', 'quantity': '2', 'total_price': '50.0'},
                {'product_id': '456', 'quantity': '3', 'total_price': '75.0'}
            ]
        }

        # Call the method under test
        result = self.orders.insert_new_order(test_order)
        self.assertEqual(result, 1)






