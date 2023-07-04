import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from flask import Flask
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
        mock_request = MagicMock(form={'data': json.dumps(mock_payload)})
        with patch('flask.request', mock_request):
            # Mock the response from the products.insert_new_product method
            mock_product_id = 1
            self.server.products.insert_new_product = MagicMock(return_value=mock_product_id)
            
            # Execute the route function
            with self.server.app.test_request_context('/insertProduct', method='POST', data={'data': json.dumps(mock_payload)}):
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