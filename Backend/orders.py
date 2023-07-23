from datetime import datetime
from typing import Any
#from contracts import contract, pre, post

""" @ref R57_0"""
# This Class is part of the @ref Model within the overall @ref ModelViewController Design.
# This class implements the methods related to orders.
class Orders:
    def __init__(self, connection) -> None:
        """
        @brief Constructor for the Orders class.   
        Initializes an instance of the Orders class with the provided database connection object.
        @param connection: The database connection object.
        """

        self.connection = connection

    #@contract
    #@post(lambda result: isinstance(result, list))
    """ @ref R57_0"""
    def get_all_orders(self) -> list:
        """
        @brief Retrieves all orders from the database.
        This method retrieves all orders from the "orders" table in the database.
        @pre The database connection must be established and valid.
        @return A list of dictionaries representing the orders. Each dictionary contains 'order_id', 'customer_name', 'total_amount', and 'datetime' details for each order.
        @post The orders_list list is populated with dictionaries representing all orders from the "orders" table.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # SQL query to retrieve all columns and rows from the "orders" table.
        query = (
            "SELECT * FROM orders")
        # Execute the SQL query using the cursor
        cursor.execute(query)
        # Initialize an empty list to store the query response
        orders_list = []
        # Iterate over the result set returned by the query and append each row to the response list as a dictionary
        for (order_id, customer_name, total_amount, dt) in cursor:
            orders_list.append({
                'order_id': order_id,
                'customer_name': customer_name,
                'total_amount': total_amount,
                'datetime': dt,
            })
        # Return the response list
        return orders_list
    
    #@contract
    #@pre(lambda order: isinstance(order, dict))
    #@post(lambda result: isinstance(result, int))
    """ @ref R59_0"""
    def insert_new_order(self, order: dict[str, Any]) -> int:
        """
        @brief Inserts a new order into the database.
        This method inserts a new order into the "orders" table in the database along with its associated order details in the "order_details" table.
        @param order: A dictionary representing the order details. It must contain 'customer_name', 'total_amount', and 'order_details' keys. The 'order_details' key must have a list of dictionaries, each representing an order detail record with 'product_id', 'quantity', and 'total_price' keys.
        @pre The database connection must be established and valid.
        @return The ID of the newly inserted order.
        @post A new order and its associated order details are inserted into the "orders" and "order_details" tables respectively. The 'order_id' of the new order is returned.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # SQL query to insert data into the 'orders' table
        query = ("INSERT INTO orders "
                 "(customer_name, total_amount, datetime)"
                 "VALUES (%s, %s, %s)")
        # Data to be inserted into the table
        data = (order['customer_name'], order['total_amount'], datetime.now())

        # Execute the SQL query with the provided data
        cursor.execute(query, data)
        order_id = cursor.lastrowid
        order_details_query = ("INSERT INTO order_details "
                           "(order_id, product_id, quantity, total_price)"
                           "VALUES (%s, %s, %s, %s)")
        
        # Initialize an empty list to store the order details data.
        order_details_data = []
        # Iterate over each order detail record in the 'order' object.
        for order_detail_record in order['order_details']:
            # Extract relevant information from the order detail record and append it to the 'order_details_data' list.
            order_details_data.append([
            order_id,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
        ])
        # Execute the SQL query 'order_details_query' using the 'cursor' object's 'executemany' method.
        cursor.executemany(order_details_query, order_details_data)
        # Commit the changes to the database
        self.connection.commit()
        # Return the last inserted row ID
        #return order_id
        return cursor.lastrowid
    
    #@contract
    #@pre(lambda order: isinstance(order, dict))
    #@post(lambda result: isinstance(result, dict))
    """ @ref R58_0"""
    def get_order_by_id(self, order_id: int) -> dict[str, Any]:
        """
        @brief Retrieves an order from the database by its order ID.
        This method retrieves a specific order from the "orders" table in the database based on the provided order_id.
        @param order_id: The ID of the order to retrieve.
        @pre The database connection must be established and valid.
        @return A dictionary representing the order. The dictionary contains 'order_id', 'customer_name', 'total_amount', and 'datetime' details for the specified order.
        @post The order dictionary is populated with the details of the order retrieved from the "orders" table based on the provided order_id.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # SQL query to retrieve a specific order by its ID
        query = (
            "SELECT * FROM orders WHERE order_id = %s"
        )
        # Execute the SQL query using the cursor and pass the order_id as a parameter
        cursor.execute(query, (order_id,))
        # Fetch the first row returned by the query
        result = cursor.fetchone()

        # Create a dictionary representing the order
        order = {
            'order_id': result[0],
            'customer_name': result[1],
            'total_amount': result[2],
            'datetime': result[3],
        }
        return order
    
    #@contract
    #@pre(lambda order: isinstance(order, dict))
    #@post(lambda result: isinstance(result, int))
    """ @ref R69_0"""
    def delete_order(self, order_id: int) -> bool:
        """
        @brief Delete an order from the database.
        This method deletes a specific order from the "orders" table in the database based on the provided order_id.
        @param order_id (int): The ID of the order to be deleted.
        @pre The database connection must be established and valid.
        @return bool: True if the order was successfully deleted, False otherwise.
        @post The order with the given order_id is deleted from the "orders" table. If the order exists and is deleted successfully, the method returns True. Otherwise, it returns False.
        """
        
        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()

        # Disable foreign key checks
        disable_fk_query = "SET FOREIGN_KEY_CHECKS = 0"
        cursor.execute(disable_fk_query)

        # SQL query to delete specific order from orders table
        query = "DELETE FROM orders WHERE order_id = %s"

        # Execute the SQL query using the cursor
        cursor.execute(query, (order_id,))

        # Get the affected row count, returns a positive number if deleted, else returns 0 if order with order_id is not found
        row_count = cursor.rowcount
        is_order_deleted = row_count > 0

        # Enable foreign key checks
        enable_fk_query = "SET FOREIGN_KEY_CHECKS = 1"
        cursor.execute(enable_fk_query)

        # Commit the changes to the database
        self.connection.commit()

        return is_order_deleted
    
    #@contract
    #@pre(lambda order: isinstance(order, dict))
    #@post(lambda result: isinstance(result, int))
    """ @ref R73_0"""
    def update_order_details(self, order_id: int, updated_amount: float) -> bool:
        """
        @brief Update the amount of an order in the database.
        This method updates the amount of a specific order in the "orders" table based on the provided order_id.
        @param order_id (int): The ID of the order to update.
        @param updated_amount (float): The updated amount of the order.
        @pre The database connection must be established and valid.
        @return bool: A boolean value indicating whether the update is successful. Returns True if the order's amount is successfully updated, False otherwise.
        @post The amount of the order with the given order_id is updated in the "orders" table. If the order with the specified order_id exists and the amount is successfully updated, the method returns True. Otherwise, it returns False.
        """
        
        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()

        # SQL query to update the amount into the 'orders' table
        query = "UPDATE orders SET amount = %s WHERE order_id = %s"

        # Execute the SQL query with the provided data
        cursor.execute(query, (updated_amount, order_id))

        # Commit the changes to the database
        self.connection.commit()

        # Get the affected row count, returns a positive number if updated else return 0 if order with order_id is
        # not found.
        row_count = cursor.rowcount

        # Assign the boolean result
        is_update_successful = True if row_count > 0 else False

        # Returns True if successful else False
        return is_update_successful








    
