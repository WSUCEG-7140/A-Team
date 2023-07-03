import unittest
from unittest.mock import MagicMock, patch
import sys
sys.path.append("..")
from sql_connection import SQLConnection
from products import Products

class TestProducts(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case.

        This method is called before each test case execution.
        """
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.products = Products(self.mock_connection)

    def test_get_all_products(self):
        """
        Test the get_all_products() method of Products.

        This test case verifies that the get_all_products() method retrieves all products
        from the database and returns the expected response.
        """

        # Set up the mock cursor and its execute method
        self.mock_cursor.__iter__.return_value = [
            (1, 'Product 1', 1, 10.0, 'Unit 1'),
            (2, 'Product 2', 2, 20.0, 'Unit 2')
        ]

        # Call the method under test
        result = self.products.get_all_products()

        # Assert the expected response
        expected_response = [
            {
                'product_id': 1,
                'name': 'Product 1',
                'unit_of_measure_id': 1,
                'price_per_unit': 10.0,
                'unit_of_measure_name': 'Unit 1'
            },
            {
                'product_id': 2,
                'name': 'Product 2',
                'unit_of_measure_id': 2,
                'price_per_unit': 20.0,
                'unit_of_measure_name': 'Unit 2'
            }
        ]
        self.assertEqual(result, expected_response)

        # Assert that the cursor and execute methods were called
        self.mock_connection.cursor.assert_called_once()
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT products.product_id, products.name, products.unit_of_measure_id, "
            "products.price_per_unit, unit_of_measures.unit_of_measure_name "
            "FROM products INNER JOIN unit_of_measures ON "
            "products.unit_of_measure_id=unit_of_measures.unit_of_measure_id"
        )









