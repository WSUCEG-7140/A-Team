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
    
    #@contract
    #@pre(lambda order: isinstance(order, dict))
    #@post(lambda result: isinstance(result, int))
    def insert_new_order(self, order):
        """
        Inserts a new order into the database.

        @param order: A dictionary representing the order details.
        @return: The ID of the newly inserted order.
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
    #@post(lambda result: isinstance(result, int))
    def get_order_by_id(self, order_id):
        """
        Retrieves an order from the database by its order ID.

        @param order_id: The ID of the order to retrieve.
        @return: A dictionary representing the order.
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

        if result:
            # Create a dictionary representing the order
            order = {
                'order_id': result[0],
                'customer_name': result[1],
                'total_amount': result[2],
                'datetime': result[3],
            }
            return order
        else:
            return None
    
    #@contract
    #@pre(lambda order: isinstance(order, dict))
    #@post(lambda result: isinstance(result, int))
    def delete_order(self, order_id):
        """
        Delete an order from the database.

        Args:
            order_id (int): The ID of the order to be deleted.

        Returns:
            bool: True if the order was successfully deleted, False otherwise.
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
        result = row_count > 0

        # Enable foreign key checks
        enable_fk_query = "SET FOREIGN_KEY_CHECKS = 1"
        cursor.execute(enable_fk_query)

        # Commit the changes to the database
        self.connection.commit()

        return result
    
    #@contract
    #@pre(lambda order: isinstance(order, dict))
    #@post(lambda result: isinstance(result, int))
    def update_order_details(self, order_id, updated_amount):
        """
        Update the amount of an order in the database.

        Args:
            order_id (int): The ID of the order to update.
            updated_amount (float): The updated amount of the order.

        Returns:
            bool: A boolean value indicating whether the update is successful.
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
        result = True if row_count > 0 else False

        # Returns True if successful else False
        return result


# def main():
#     """
#     Entry point of the program.
#     """
#     connection = SQLConnection()
#     connection = connection.connect()

#     orders = Orders(connection)
#     orders.get_all_orders()

# if __name__ == '__main__':
#     main()








    
