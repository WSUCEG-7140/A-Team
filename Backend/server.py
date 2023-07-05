from flask import Flask, request, jsonify
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Backend.sql_connection import SQLConnection
import json
from Backend.products import Products
from Backend.orders import Orders


# from contracts import contract, pre, post

class Server:
    def __init__(self):
        """
        Initializes the Server class.
        """
        self.app = Flask(__name__)  # Creates a Flask application
        self.connection = SQLConnection()  # Establishes a SQL connection
        self.products = Products(self.connection)  # Creates an instance of the Products class with the SQL connection
        self.orders = Orders(self.connection)  # Creates an instance of the Orders class with the SQL connection

    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run()  # Starts the Flask application

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    def get_all_products(self):
        """
        Retrieves all products from the database.

        Returns:
            Flask Response: JSON response containing all products.
        """
        response = self.products.get_all_products()  # Retrieves all products from the database
        response = jsonify(response)  # Converts the response to a JSON object
        response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return response

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    def insert_new_product(self):
        """
        Inserts a new product into the database.

        Returns:
            Flask Response: JSON response containing the inserted product ID.
        """
        request_payload = json.loads(request.form['data'])  # Parses the request payload as JSON
        product_id = self.products.insert_new_product(request_payload)  # Inserts the new product into the database
        response = jsonify({'product_id': product_id})  # Creates a JSON response with the inserted product ID
        response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return response

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    def get_all_orders(self):
        """
        Retrieves all orders from the database.

        Returns:
            Flask Response: JSON response containing all orders.
        """
        response = self.orders.get_all_orders()  # Retrieves all orders from the database
        response = jsonify(response)  # Converts the response to a JSON object
        response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return response

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    def insert_new_order(self):
        """
        Inserts a new order into the database.

        Returns:
            Flask Response: JSON response containing the inserted order ID.
        """
        request_payload = json.loads(request.form['data'])  # Parses the request payload as JSON
        order_id = self.orders.insert_new_order(request_payload)  # Inserts the new order into the database
        response = jsonify({'order_id': order_id})  # Creates a JSON response with the inserted order ID
        response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return response

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    def get_sales_report(self):
        """

        Retrieves the sales report by report type between the specified dates.

        Returns:
            Flask Response: JSON response containing sales report by report type.
        """
        report_type = request.args.get('report_type')  # Get report_type from request.
        start_date = request.args.get('start_date')  # Get start_date from request.
        end_date = request.args.get('end_date')  # Get end_date from request.
        if report_type == 'total_sales':
            response = self.products.total_sales(start_date, end_date)  # Generates total sales report.
        elif report_type == 'top_selling_products':
            response = self.products.top_selling_products(start_date, end_date)  # Generates sales report by top five
            # selling products.
        elif report_type == 'sales_by_category':
            response = self.products.sales_by_category(start_date, end_date)  # Generates sales report by category.
        response = jsonify(response)  # Converts the response to a JSON object
        response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return response

    def setup_routes(self):
        """
        Sets up the routes for the Flask application.
        """
        self.app.route('/getProducts', methods=['GET'])(
            self.get_all_products)  # Sets up a route for getting all products
        self.app.route('/insertProduct', methods=['POST'])(
            self.insert_new_product)  # Sets up a route for inserting a new product
        self.app.route('/getOrders', methods=['GET'])(self.get_all_orders)  # Sets up a route for getting all orders
        self.app.route('/insertOrder', methods=['POST'])(
            self.insert_new_order)  # Sets up a route for inserting a new order
        self.app.route('/salesReport', methods=['GET'])(
            self.get_sales_report)  # Sets up a route for generating sales report


if __name__ == '__main__':
    app = Server()  # Creates an instance of the Server class
    app.setup_routes()  # Sets up the routes for the Flask application
    app.run()  # Starts the Flask application