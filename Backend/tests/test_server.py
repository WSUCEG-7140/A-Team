import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
import pytest
from flask import Flask, jsonify
import json
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Backend.server import Server
from Backend.products import Products
from Backend.orders import Orders


# Define a test case class derived from unittest.TestCase
class ServerTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by initializing necessary objects and dependencies.
        """
        self.app = Flask(__name__)
        self.server = Server()
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.products = Products(self.mock_connection)
        self.orders = Orders(self.mock_connection)
        self.server.app = self.app
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Clean up resources after each test case.
        """
        pass

    def test_run(self):
        """
        Test the run() method of the server.

        @returns: None
        """

        # Patching the 'run' method of the Flask class to create a mock object.
        with patch.object(Flask, 'run') as mock_run:
            # Invoking the 'run' method of the server.
            self.server.run()
            # Verifying that the 'run' method of Flask was called exactly once.
            mock_run.assert_called_once()

    def test_setup_routes(self):
        """
        Test the setup_routes() method of the server.

        @returns: None
        """

        # Invoking the 'setup_routes' method of the 'self.server' object to set up routes.
        self.server.setup_routes()
        # Extracting the rules from the URL map of the Flask app and storing them in the 'routes' variable.
        routes = [r.rule for r in self.app.url_map.iter_rules()]
        # Asserting that the '/getProducts' route is present in the 'routes' list.
        self.assertIn('/getProducts', routes)
        # Asserting that the '/insertProduct' route is present in the 'routes' list.
        self.assertIn('/insertProduct', routes)
        # Asserting that the '/getOrders' route is present in the 'routes' list.
        self.assertIn('/getOrders', routes)
        # Asserting that the '/insertOrder' route is present in the 'routes' list.
        self.assertIn('/insertOrder', routes)
        # Asserting that the '/salesReport' route is present in the 'routes' list.
        self.assertIn('/salesReport', routes)
        # Asserting that the '/searchProduct' route is present in the 'route' list.
        self.assertIn('/searchProduct', routes)
        # Asserting that the '/updateProductInformation/<int:product_id>' route is present in the
        # 'routes' list.
        self.assertIn('/updateProductInformation/<int:product_id>', routes)
        # Asserting that the '/removeProduct/<int:product_id>' route is present in the
        # 'routes' list.
        self.assertIn('/removeProduct/<int:product_id>', routes)
        # Asserting that the '/getOrderById' route is present in the
        # 'routes' list.
        self.assertIn('/getOrderById', routes)
        # Asserting that the '/removeOrder/<int:order_id>' route is present in the
        # 'routes' list.
        self.assertIn('/removeOrder/<int:order_id>', routes)
        # Asserting that the 'updateOrderInformation/<int:order_id>' route is present in the
        # 'routes' list.
        self.assertIn('/updateOrderInformation/<int:order_id>', routes)

    def test_get_all_products(self):
        """
        Test the get_all_products() method of the server.

        @returns: None
        """

        # Mock the response from the server.get_all_products method
        mock_response = [{'id': 1, 'name': 'Product 1'}, {'id': 2, 'name': 'Product 2'}]
        self.server.products.get_all_products = MagicMock(return_value=mock_response)

        # Mock the request and execute the route function
        with self.server.app.test_request_context('/getProducts', method='GET'):
            response = self.server.get_all_products()

            # Assert that the response is correct
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), mock_response)
            self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')

    def test_insert_new_product(self):
        """
        Test the insert_new_product() method of the server.

        @returns: None
        """

        # Mock the request payload
        mock_payload = {'name': 'New Product'}
        mock_request = MagicMock(json=mock_payload)
        with patch('flask.request', mock_request):
            # Mock the response from the products.insert_new_product method
            mock_product_id = 1
            self.server.products.insert_new_product = MagicMock(return_value=mock_product_id)

            # Execute the route function
            with self.server.app.test_request_context('/insertProduct', method='POST',
                                                      data={'data': json.dumps(mock_payload)}):
                response = self.server.insert_new_product()

                # Assert that the response is correct
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), {'product_id': mock_product_id})
                self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')

    def test_get_all_orders(self):
        # Mock the response from the orders.get_all_orders method
        mock_response = [{'order_id': 1, 'customer_name': 'Customer 1'}, {'order_id': 2, 'customer_name': 'Customer 2'}]
        self.server.orders.get_all_orders = MagicMock(return_value=mock_response)

        # Execute the route function
        with self.server.app.test_request_context('/getOrders', method='GET'):
            response = self.server.get_all_orders()

            # Assert that the response is correct
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), mock_response)
            self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')

    def test_insert_new_order(self):
        """
        Test the insert_new_order() method of the server.

        @returns: None
        """
        # Mock the request payload
        mock_payload = {
            'customer_name': 'John Doe',
            'total_amount': 100.0,
            'order_details': [
                {'product_id': 1, 'quantity': 2, 'total_price': 20.0},
                {'product_id': 2, 'quantity': 3, 'total_price': 30.0}
            ]
        }
        mock_request = mock.MagicMock(form={'data': json.dumps(mock_payload)})
        with mock.patch('flask.request', mock_request):
            # Mock the response from the orders.insert_new_order method
            mock_order_id = 1
            self.server.orders.insert_new_order = mock.MagicMock(return_value=mock_order_id)

            # Execute the route function
            with self.server.app.test_request_context('/insertOrder', method='POST',
                                                      data={'data': json.dumps(mock_payload)}):
                response = self.server.insert_new_order()

                # Assert that the response is correct
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), {'order_id': mock_order_id})
                self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')

    def test_remove_product(self):
        """
        Test the remove_product() route of the server
        This test case verifies that the remove_product() route returns the correct response
        for both successful and failed removal.

        returns: None
        """
        # Define test cases with different inputs and different outputs
        test_cases =[
            (True, {'success': True, 'message': 'Product Removed Successfully.'}),
            (False, {'success': False, 'message': 'Failed to Remove Product.'})
        ]
        # Iterate over the test cases
        for result, expected_response in test_cases:

            mock_result = result
            self.server.products.delete_product = MagicMock(return_value=mock_result)

            # Execute the route function
            with self.server.app.test_request_context('/removeProduct/1', method='POST',):
                response = self.server.remove_product(1)

                # Assert that the response is correct
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), expected_response)
                self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')

    def test_update_product_information(self):
        """
        Test the update_product_information() route of the server
        This test case verifies that the update_product_information() route returns the correct response
        for both successful and failed updates.

        returns: None
        """
        # Define test cases with different inputs and different outputs
        test_cases =[
            (10.99, True, {'success': True, 'message': 'Product Details Updated Successfully.'}),
            (20.65, False, {'success': False, 'message': 'Failed to Update Product Details.'})
        ]
        # Iterate over the test cases
        for price, result, expected_response in test_cases:
            # Mock the request JSON data
            mock_payload = {'price_per_unit' : price}
            mock_request = MagicMock(json=mock_payload)
            with patch('flask.request', mock_request):
                # Mock the response from the products.update_product_details method.
                mock_result = result
                self.server.products.update_product_details = MagicMock(return_value=mock_result)

                # Execute the route function
                with self.server.app.test_request_context('/updateProductInformation/1', method='POST',
                                                      json=mock_payload):
                    response = self.server.update_product_information(1)

                    # Assert that the response is correct
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.get_json(), expected_response)
                    self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')

    def test_get_sales_report(self):
        """
        Test the get_sales_report() method of the server.
        """
        # Define the list of report types
        report_types = ['total_sales', 'top_selling_products', 'sales_by_category']

        # Mock the request parameters
        mock_start_date = '2023-01-01'
        mock_end_date = '2023-06-30'

        for report_type in report_types:
            # Mock the request for the current report type
            mock_request = MagicMock(
                args={'report_type': report_type, 'start_date': mock_start_date, 'end_date': mock_end_date})

            # Mock the response from the corresponding products method
            mock_response = [
                {'order_id': 1, 'customer_name': 'Blake C', 'datetime': '2023-05-20', 'total_amount': 20.00},
                {'order_id': 2, 'customer_name': 'Usha A', 'datetime': '2023-05-26', 'total_amount': 10.00},
                {'total_sales': 30.00}
            ]

            # Mock the request and execute the route function
            with self.server.app.test_request_context('/salesReport', method='GET', query_string=mock_request.args):
                # Patch the corresponding report generation method
                with patch.object(self.server.products, report_type, return_value=mock_response):
                    # Call the get_sales_report() method
                    response = self.server.get_sales_report()
                    # Assert that the response is correct
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.get_json(), mock_response)
                    self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')
          
    def test_search_products(self):
        """
        Test the search_products() method of the server.

        This test case verifies that the search_products() method correctly handles the request
        to search for a specific product name and returns the expected JSON response.
        """

        # Set up the input parameters
        product_name = 'Product 1'

        # Mock the response from the server.products.search_products method
        mock_response = {
        'product_id': 1,
        'name': 'Product 1',
        'unit_of_measure_id': 1,
        'price_per_unit': 10.0,
        'unit_of_measure_name': 'Unit 1'
        }
        self.server.products.search_products = MagicMock(return_value=mock_response)

        # Use the test client to make requests within the application context
        with self.server.app.test_request_context('/searchProduct', method='GET'):
        # Make the request to the searchProducts endpoint
            response = self.server.search_products()

            # Assert that the response is correct
            expected_response = jsonify(mock_response)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), expected_response.get_json())
            self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')

    def test_get_order_by_id(self):
        # Mock the response from the orders.get_order_by_id method
        order_id = 1
        mock_order = {'order_id': 1, 'customer_name': 'Customer 1'}
        self.server.orders.get_order_by_id = MagicMock(return_value=mock_order)

        # Execute the route function
        with self.server.app.test_request_context(f'/getOrder/{order_id}', method='GET'):
            response = self.server.get_order_by_id(order_id)

            # Assert that the response is correct
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['order_id'], order_id)
            self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')
    
    def test_remove_order(self):
        """
        Test the remove_order() route of the server.
        This test case verifies that the remove_order() route returns the correct response
        for both successful and failed removal.

        returns: None
        """
        # Define test cases with different inputs and different outputs
        test_cases = [
            (True, {'success': True, 'message': 'Order Removed Successfully.'}),
            (False, {'success': False, 'message': 'Failed to Remove Order.'})
        ]

        # Iterate over the test cases
        for result, expected_response in test_cases:

            mock_result = result
            self.server.orders.delete_order = MagicMock(return_value=mock_result)

            # Execute the route function
            with self.server.app.test_request_context('/removeOrder/1', method='POST'):
                response = self.server.remove_order(1)

                # Assert that the response is correct
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), expected_response)
                self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')


