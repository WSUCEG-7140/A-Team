from datetime import datetime
#from sql_connection import SQLConnection
#from contracts import contract, pre, post

class Orders:
    def __init__(self, connection):
        """
        Constructor for Orders class.

        @param connection: The database connection object.
        """
        self.connection = connection

    #@contract
    #@post(lambda result: isinstance(result, list))
    def get_all_orders(self):
        """
        Retrieves all orders from the database.

        @return: A list of dictionaries representing the orders.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # SQL query to retrieve all columns and rows from the "orders" table.
        query = (
            "SELECT * FROM orders")
        # Execute the SQL query using the cursor
        cursor.execute(query)
        # Initialize an empty list to store the query response
        response = []
        # Iterate over the result set returned by the query and append each row to the response list as a dictionary
        for (order_id, customer_name, total_amount, dt) in cursor:
            response.append({
                'order_id': order_id,
                'customer_name': customer_name,
                'total_amount': total_amount,
                'datetime': dt,
            })
        # Return the response list
        return response