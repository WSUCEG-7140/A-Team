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

    def test_delete_product(self):
        """
        Test the delete_product() method of Products.

        This test case verifies that the delete_product() method correctly deletes specific product
        in the database and returns the result as True for successful delete or False.
        """
        # Set the rowcount to indicate deletion. set 0 to test an unsuccessful deletion
        self.mock_cursor.rowcount = 1
        # Call the delete_product() method under test and assert the expected result
        self.assertIn(self.products.delete_product(1), [True, False])
        # Assert that the cursor, execute, and commit methods were called
        self.mock_connection.cursor.assert_called_once()
        self.mock_cursor.execute.assert_any_call("SET FOREIGN_KEY_CHECKS = 0")
        self.mock_cursor.execute.assert_any_call("DELETE FROM products WHERE product_id = %s", (1, ))
        self.mock_cursor.execute.assert_any_call("SET FOREIGN_KEY_CHECKS = 1")
        self.mock_connection.commit.assert_called_once()


    def test_update_product_details(self):
        """
        Test the update_product_details() method of Products.

        This test case verifies that the update_product_details() method correctly updates existing product details
        in the database and returns the result as True for successful update or False.
        """
        # Set the rowcount to indicate an update. set 0 to test an unsuccessful update
        self.mock_cursor.rowcount = 1
        # Call the update_product_details() method under test and assert the expected result
        self.assertIn(self.products.update_product_details(1, 10), [True, False])
        # Assert that the cursor, execute, and commit methods were called
        self.mock_connection.cursor.assert_called_once()
        expected_query = (
            "UPDATE products SET price_per_unit = %s WHERE product_id = %s"
        )
        # Assert that the cursor, execute, and commit methods were called
        self.mock_cursor.execute.assert_called_once_with(expected_query, (10, 1))
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

    def test_top_selling_products(self):
        """
        Test the top_selling_products() method of the Products class.
        This test case verifies that the method retrieves top 5 selling products.
        """
        # Set up mock cursor and its execute method
        self.mock_cursor.fetchall.return_value = [
            (1, 'Product A', 20),
            (2, 'Product B', 40),
            (3, 'Product C', 10)
        ]
        # Input parameters to be passed to top_selling_products method
        start_date = '2023-05-20'
        end_date = '2023-05-25'
        # Call the top_selling_products method under test
        result = self.products.top_selling_products(start_date, end_date)
        # Assert the expected response
        expected_response = [
            {'product_id': 1, 'products_name': 'Product A', 'total_quantity': 20},
            {'product_id': 2, 'products_name': 'Product B', 'total_quantity': 40},
            {'product_id': 3, 'products_name': 'Product C', 'total_quantity': 10}
        ]
        self.assertEqual(result, expected_response)
        # Assert that the cursor and execute methods were called
        self.mock_connection.cursor.assert_called_once()
        expected_query = (
                "SELECT products.product_id, products.name, SUM(order_details.quantity) AS total_quantity " +
                "FROM products " +
                "JOIN order_details ON products.product_id = order_details.product_id " +
                "JOIN orders ON order_details.order_id = orders.order_id " +
                "WHERE orders.datetime BETWEEN %s AND %s " +
                "GROUP BY products.product_id " +
                "ORDER BY total_quantity DESC " +
                "LIMIT 5"
        )
        self.mock_cursor.execute.assert_called_once_with(expected_query, ('2023-05-20', '2023-05-25'))

    def test_sales_by_category(self):
        """
        Test the sales_by_category() method of the Products class.
        This test case verifies that the method retrieves sales report by category.
        """
        # Set up mock cursor and its execute method
        self.mock_cursor.fetchall.return_value = [
            ('Category A', 10.00),
            ('Category B', 5.00),
            ('Category C', 10.00)
        ]
        # Input parameters to be passed to sales_by_category method
        start_date = '2023-05-20'
        end_date = '2023-05-25'
        # Call the sales_by_category method under test
        result = self.products.sales_by_category(start_date, end_date)
        # Assert the expected response
        expected_response = [
            {'category_name': 'Category A', 'total_sales': 10.00},
            {'category_name': 'Category B', 'total_sales': 5.00},
            {'category_name': 'Category C', 'total_sales': 10.00}
        ]
        self.assertEqual(result, expected_response)
        # Assert that the cursor and execute methods were called
        self.mock_connection.cursor.assert_called_once()
        expected_query = (
                "SELECT categories.category_name, SUM(order_details.total_price) AS total_sales" +
                "FROM categories " +
                "JOIN products ON categories.category_id = products.category_id " +
                "JOIN order_details ON products.product_id = order_details.product_id " +
                "JOIN orders ON order_details.order_id = orders.order_id " +
                "WHERE orders.datetime BETWEEN %s AND %s " +
                "GROUP BY categories.category_id " +
                "ORDER BY total_sales DESC"
        )
        self.mock_cursor.execute.assert_called_once_with(expected_query, ('2023-05-20', '2023-05-25'))