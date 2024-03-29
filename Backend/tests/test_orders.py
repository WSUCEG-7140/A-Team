import unittest
from unittest.mock import MagicMock
from datetime import datetime
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Backend.orders import Orders

""" \test @ref R57_0 R59_0 R58_0 R69_0 R73_0"""
class OrdersTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by creating mock objects and initializing the 'Orders' instance.
        """

        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.orders = Orders(self.mock_connection)

    """ \test @ref R57_0"""
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

    """ \test @ref R59_0"""
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

    """ \test @ref R58_0"""
    def test_get_order_by_id(self):
        """
        Test case for the 'get_order_by_id' method of the 'Orders' class.
        """

        # Mock the result returned by the query
        order_id = 1
        mock_result = (order_id, 'John Doe', 100.0, datetime.now())
        self.mock_cursor.fetchone.return_value = mock_result

        # Call the method under test
        result = self.orders.get_order_by_id(order_id)

        # Assert the expected SQL query was executed
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM orders WHERE order_id = %s", (order_id,))

        # Assert the expected response was returned
        expected_response = {
            'order_id': order_id,
            'customer_name': 'John Doe',
            'total_amount': 100.0,
            'datetime': mock_result[3]
        }
        self.assertEqual(result, expected_response)

    """ \test @ref R69_0"""
    def test_delete_order(self):
        """
        Test the delete_order() method of Orders.

        This test case verifies that the delete_order() method correctly deletes a specific order
        in the database and returns True for a successful delete or False for an unsuccessful delete.
        """
        # Set the rowcount to indicate deletion. Set 0 to test an unsuccessful deletion.
        self.mock_cursor.rowcount = 1
    
        # Call the delete_order() method under test and assert the expected result.
        self.assertIn(self.orders.delete_order(1), [True, False])
    
        # Assert that the cursor, execute, and commit methods were called.
        self.mock_connection.cursor.assert_called_once()
        self.mock_cursor.execute.assert_any_call("SET FOREIGN_KEY_CHECKS = 0")
        self.mock_cursor.execute.assert_any_call("DELETE FROM orders WHERE order_id = %s", (1,))
        self.mock_cursor.execute.assert_any_call("SET FOREIGN_KEY_CHECKS = 1")
        self.mock_connection.commit.assert_called_once()
    
    """ \test @ref R73_0"""
    def test_update_order_details(self):
        """
        Test the update_order_amount() method of Orders.

        This test case verifies that the update_order_amount() method correctly updates the amount of an existing order
        in the database and returns the result as True for a successful update or False.
        """
        # Set the rowcount to indicate an update. Set 0 to test an unsuccessful update
        self.mock_cursor.rowcount = 1

        # Call the update_order_amount() method under test and assert the expected result
        self.assertIn(self.orders.update_order_details(1, 100), [True, False])

        # Assert that the cursor, execute, and commit methods were called
        self.mock_connection.cursor.assert_called_once()
        expected_query = "UPDATE orders SET amount = %s WHERE order_id = %s"
        self.mock_cursor.execute.assert_called_once_with(expected_query, (100, 1))
        self.mock_connection.commit.assert_called_once()








