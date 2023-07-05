import unittest
from unittest.mock import MagicMock
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Backend.products import Products


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

    def test_insert_new_product(self):
        """
        Test the insert_new_product() method of Products.

        This test case verifies that the insert_new_product() method correctly inserts a new product
        into the database and returns the ID of the inserted product.
        """

        # Set up the mock cursor and its execute method
        self.mock_cursor.lastrowid = 1

        # Call the method under test
        result = self.products.insert_new_product({
            'name': 'mango',
            'unit_of_measure_id': '1',
            'price_per_unit': 10
        })

        # Assert the expected result
        self.assertEqual(result, 1)

        # Assert that the cursor, execute, and commit methods were called
        self.mock_connection.cursor.assert_called_once()
        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO products (name, unit_of_measure_id, price_per_unit)VALUES (%s, %s, %s)",
            ('mango', '1', 10)
        )
        self.mock_connection.commit.assert_called_once()

    def test_total_sales(self):
        """
        Test the total_sales() method.
        This test case verifies the total_sales method returns the sales report based on total sales between the specified dates.
        """
        # Set up mock cursor and its execute method
        self.mock_cursor.fetchall.return_value = [
            (1, 'Person A', '2023-05-20', 20.00),
            (2, 'Person B', '2023-05-24', 40.00),
            (3, 'Person C', '2023-05-24', 10.00)
        ]
        # Input parameters to be passed to total_sales method
        start_date = '2023-05-20'
        end_date = '2023-05-25'
        # Call the total_sales method under test
        result = self.products.total_sales(start_date, end_date)
        # Assert the expected response
        expected_response = [
            {'order_id': 1, 'customer_name': 'Person A', 'datetime': '2023-05-20', 'total_amount': 20.00},
            {'order_id': 2, 'customer_name': 'Person B', 'datetime': '2023-05-24', 'total_amount': 40.00},
            {'order_id': 3, 'customer_name': 'Person C', 'datetime': '2023-05-24', 'total_amount': 10.00},
            {'total_sales': 70.00}
        ]
        self.assertEqual(result, expected_response)
        # Assert that the cursor and execute methods were called
        self.mock_connection.cursor.assert_called_once()
        expected_query = (
                "SELECT order_id, customer_name, datetime, total_amount " +
                "FROM orders " +
                "WHERE datetime BETWEEN %s AND %s GROUP BY order_id, customer_name")
        self.mock_cursor.execute.assert_called_once_with(expected_query, ('2023-05-20', '2023-05-25'))

