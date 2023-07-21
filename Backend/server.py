from flask import Flask, request, jsonify
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Backend.sql_connection import SQLConnection
import json
from Backend.products import Products
from Backend.orders import Orders
from Backend.unit_of_measures import UnitOfMeasures
# from contracts import contract, pre, post

""" @ref R6_0"""
# This Class is part of the @ref Controller within the overall @ref ModelViewController Design.
# This class implements API endpoints for methods related to orders, products, unit_of_measures.
class Server:
    """ @ref R6_0"""
    def __init__(self):
        """
        @brief Initializes the Server class.
        """
        self.app = Flask(__name__)  # Creates a Flask application
        self.connection = SQLConnection()  # Establishes a SQL connection
        self.products = Products(self.connection)  # Creates an instance of the Products class with the SQL connection
        self.orders = Orders(self.connection)  # Creates an instance of the Orders class with the SQL connection
        self.unit_of_measures = UnitOfMeasures(self.connection) # Creates an instance of the unit_of_measure class with the SQL connection

    """ @ref R6_0"""
    def run(self):
        """
        @brief Runs the Flask application.
        """
        self.app.run()  # Starts the Flask application

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R6_0"""
    def get_all_products(self):
        """
        @brief Retrieves all products from the database.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing all products.
        @post The method retrieves all products from the database, converts the response to a JSON object, and adds the necessary header to allow cross-origin requests before returning the response.
        """
        
        products_data = self.products.get_all_products()  # Retrieves all products from the database
        json_response = jsonify(products_data)  # Converts the response to a JSON object
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R7_0"""
    def insert_new_product(self):
        """
        @brief Inserts a new product into the database.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing the inserted product ID.
        @post The method inserts the new product into the database and returns a JSON response containing the inserted product ID. The response includes the necessary header to allow cross-origin requests.
        """

        request_payload = json.loads(request.form['data'])  # Parses the request payload as JSON
        product_id = self.products.insert_new_product(request_payload)  # Inserts the new product into the database
        json_response = jsonify({'product_id': product_id})  # Creates a JSON response with the inserted product ID
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R57_0"""
    def get_all_orders(self):
        """
        @brief Retrieves all orders from the database.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing all orders.
        @post The method retrieves all orders from the database, converts the response to a JSON object, and adds the necessary header to allow cross-origin requests before returning the response.
        """

        orders_data = self.orders.get_all_orders()  # Retrieves all orders from the database
        json_response = jsonify(orders_data )  # Converts the response to a JSON object
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R59_0"""
    def insert_new_order(self):
        """
        @brief Inserts a new order into the database.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing the inserted order ID.
        @post The method inserts the new order into the database and returns a JSON response containing the inserted order ID. The response includes the necessary header to allow cross-origin requests.
        """

        request_payload = json.loads(request.form['data'])  # Parses the request payload as JSON
        order_id = self.orders.insert_new_order(request_payload)  # Inserts the new order into the database
        json_response = jsonify({'order_id': order_id})  # Creates a JSON response with the inserted order ID
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R9_0"""
    def remove_product(self, product_id):
        """
        @brief Remove a specific product from the database.
        @param product_id: The ID of the product to be removed from the database.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing the message indicating the success or failure of the removal.
        @post The method removes the product from the database based on the provided product ID and returns a JSON response containing a success message if the removal is successful, or a failure message if the removal fails. The response includes the necessary header to allow cross-origin requests.
        """

        removal_result = self.products.delete_product(product_id)  # Removes product from the database
        if removal_result is True:
            json_response = jsonify({'success': True, 'message': 'Product Removed Successfully.'}) # Creates a JSON response with a message.
        else:
            json_response = jsonify({'success': False, 'message': 'Failed to Remove Product.'}) # Creates a JSON response with a message.
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response


    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R8_0"""
    def update_product_information(self, product_id):
        """
        @brief Update existing product information in the database.
        @param product_id: The ID of the product to be updated with the new price details.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing the message indicating the success or failure of the update.
        @post The method updates the product information in the database based on the provided product ID and the new price_per_unit value. It returns a JSON response containing a success message if the update is successful, or a failure message if the update fails. The response includes the necessary header to allow cross-origin requests.
        """

        updated_price = request.json.get('price_per_unit')
        update_result = self.products.update_product_details(product_id, updated_price)  # Updates product information in the database
        if update_result is True:
            json_response = jsonify({'success': True, 'message': 'Product Details Updated Successfully.'}) # Creates a JSON response with a message.
        else:
            json_response = jsonify({'success': False, 'message': 'Failed to Update Product Details.'}) # Creates a JSON response with a message.
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R34_0"""
    def get_sales_report(self):
        """
        @brief Retrieves the sales report by report type between the specified dates.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing the sales report by the specified report type.
        @post The method generates the sales report based on the provided report_type, start_date, and end_date. It returns a JSON response containing the sales report by the specified report type. The response includes the necessary header to allow cross-origin requests.
        """
        
        report_type = request.args.get('report_type')  # Get report_type from request.
        start_date = request.args.get('start_date')  # Get start_date from request.
        end_date = request.args.get('end_date')  # Get end_date from request.
        if report_type == 'total_sales':
            sales_report = self.products.total_sales(start_date, end_date)  # Generates total sales report.
        elif report_type == 'top_selling_products':
            sales_report = self.products.top_selling_products(start_date, end_date)  # Generates sales report by top five
            # selling products.
        elif report_type == 'sales_by_category':
            sales_report = self.products.sales_by_category(start_date, end_date)  # Generates sales report by category.
        json_response = jsonify(sales_report)  # Converts the response to a JSON object
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response
    
    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R10_0"""
    def search_products(self):
        """
        @brief Search for a product name in the database.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing the product information if found.
        @post The method searches for the product name in the database and returns a JSON response containing the product information if found. The response includes the necessary header to allow cross-origin requests.
        """
        
        product_name = request.args.get('product_name', '')  # Get the 'product_name' parameter from the request
        search_product_result = self.products.search_products(product_name)  # Call the search_products method with the provided product name
        json_response = jsonify(search_product_result)  # Converts the response to a JSON object
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response

    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R58_0"""
    def get_order_by_id(self, order_id):
        """
        @brief Retrieves an order from the database by its ID.
        @param order_id (int): The ID of the order to retrieve.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing the order information.
        @post The method retrieves the order from the database based on the given 'order_id'. It converts the order information into a JSON response and includes the necessary header to allow cross-origin requests.
        """
        
        order = self.orders.get_order_by_id(order_id)  # Retrieves the order from the database by ID
        json_response = jsonify(order)  # Converts the order to a JSON object
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response
    
    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R73_0"""
    def update_order_information(self, order_id):
        """
        @brief Update existing order information in the database.
        @param order_id: The ID of the order to be updated with the new amount details.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing the message indicating the success or failure of the update.
        @post The method updates the order information in the database based on the provided order ID and the new amount. It returns a JSON response containing a success message if the update is successful, or a failure message if the update fails. The response includes the necessary header to allow cross-origin requests.
        """

        updated_amount = request.json.get('amount')
        update_result = self.orders.update_order_details(order_id, updated_amount)  # Updates order information in the database
        if update_result is True:
            json_response = jsonify({'success': True, 'message': 'Order Details Updated Successfully.'})  # Creates a JSON response with a message.
        else:
            json_response = jsonify({'success': False, 'message': 'Failed to Update Order Details.'})  # Creates a JSON response with a message.
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response
    
    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R69_0"""
    def remove_order(self, order_id):
        """
        @brief Remove a specific order from the database.
        @param order_id: The ID of the order to be removed from the database.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing the message indicating the success or failure of the removal.
        @post The method removes the order from the database based on the provided order ID and returns a JSON response containing a success message if the removal is successful, or a failure message if the removal fails. The response includes the necessary header to allow cross-origin requests.
        """

        removal_result = self.orders.delete_order(order_id)  # Removes the order from the database
        if removal_result is True:
            json_response = jsonify({'success': True, 'message': 'Order Removed Successfully.'})  # Creates a JSON response with a message.
        else:
            json_response = jsonify({'success': False, 'message': 'Failed to Remove Order.'})  # Creates a JSON response with a message.
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response
    
    # @contract
    # @post(lambda result: isinstance(result, Flask.Response), "The return value must be a Flask Response object.")
    """ @ref R71_0"""
    def get_unit_of_measures(self):
        """
        @brief Retrieves all unit_of_measures from the database.
        @pre The database connection must be established and valid.
        @return Flask Response: JSON response containing all orders.
        @post The method retrieves all unit_of_measures from the database, converts the response to a JSON object, and adds the necessary header to allow cross-origin requests before returning the response.
        """

        unit_of_measures_data = self.unit_of_measures.get_unit_of_measures()  # Retrieves all unit_of_measures from the database
        json_response = jsonify(unit_of_measures_data)  # Converts the response to a JSON object
        json_response.headers.add('Access-Control-Allow-Origin', '*')  # Adds a header to allow cross-origin requests
        return json_response
    
    """ @ref R6_0"""
    def setup_routes(self):
        """
        @brief Sets up the routes for the Flask application.
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
        self.app.route('/searchProduct', methods=['GET'])(
            self.search_products) # Sets up a route to search product from the database
        self.app.route('/updateProductInformation/<int:product_id>', methods=['POST'])(
            self.update_product_information) # Sets up a route to update details of existing products.
        self.app.route('/removeProduct/<int:product_id>', methods=['POST'])(
            self.remove_product)  # Sets up a route to remove product from the database
        self.app.route('/getOrderById', methods=['GET'])(
            self.get_order_by_id) # Sets up a route to get order by id from the database
        self.app.route('/removeOrder/<int:order_id>', methods=['POST'])(
            self.remove_order) # Sets up a route to remove order from the database
        self.app.route('/updateOrderInformation/<int:order_id>', methods=['POST'])(
            self.update_order_information) # Sets up a route to update order from the database
        self.app.route('/getUnitOfMeasures', methods=['GET'])(
            self.get_unit_of_measures) # Sets up a route to update order from the database

if __name__ == '__main__':
    """
    this section is typically executed when the script is run directly, it is challenging to write test cases to cover this part of the code as 
    it starts the Flask application, which runs indefinitely and blocks further code execution.
    """
    app = Server()  # Creates an instance of the Server class
    app.setup_routes()  # Sets up the routes for the Flask application
    app.run()  # Starts the Flask application
