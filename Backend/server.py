from flask import Flask, request, jsonify
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Backend.sql_connection import SQLConnection
import json
from Backend.products import Products
from Backend.orders import Orders
#from contracts import contract, pre, post

class Server:
    def __init__(self):
        """
        Initializes the Server class.
        """
        self.app = Flask(__name__)    # Creates a Flask application
        self.connection = SQLConnection()   # Establishes a SQL connection
        self.products = Products(self.connection)  # Creates an instance of the Products class with the SQL connection
        self.orders = Orders(self.connection)  # Creates an instance of the Orders class with the SQL connection

    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run()  # Starts the Flask application

    #@contract
    #@post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    def get_all_products(self):
        """
        Retrieves all products from the database.

        Returns:
            Flask Response: JSON response containing all products.
        """
        response = self.products.get_all_products()   # Retrieves all products from the database
        response = jsonify(response)  # Converts the response to a JSON object
        response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return response

    #@contract
    #@post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    def insert_new_product(self):
        """
        Inserts a new product into the database.

        Returns:
            Flask Response: JSON response containing the inserted product ID.
        """
        request_payload = json.loads(request.form['data'])  # Parses the request payload as JSON
        product_id = self.products.insert_new_product(request_payload) # Inserts the new product into the database
        response = jsonify({'product_id': product_id})  # Creates a JSON response with the inserted product ID
        response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return response
    
    #@contract
    #@post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    def get_all_orders(self):
        """
        Retrieves all orders from the database.

        Returns:
            Flask Response: JSON response containing all orders.
        """
        response = self.orders.get_all_orders()   # Retrieves all orders from the database
        response = jsonify(response)  # Converts the response to a JSON object
        response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return response

    def setup_routes(self):
        """
        Sets up the routes for the Flask application.
        """
        self.app.route('/getProducts', methods=['GET'])(self.get_all_products)   # Sets up a route for getting all products
        self.app.route('/insertProduct', methods=['POST'])(self.insert_new_product)  # Sets up a route for inserting a new product
        self.app.route('/getOrders', methods=['GET'])(self.get_all_orders)   # Sets up a route for getting all orders

if __name__ == '__main__':
    app = Server()   # Creates an instance of the Server class
    app.setup_routes()  # Sets up the routes for the Flask application
    app.run() # Starts the Flask application