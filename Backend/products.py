from sql_connection import SQLConnection
# from contracts import contract, pre, post

from itertools import product


class Products:
    def __init__(self, connection):
        """
        Constructor for Products class.

        @param connection: The database connection object.
        """
        self.connection = connection

    # @contract
    # @post(lambda result: isinstance(result, list), "The return value must be a list.")
    def get_all_products(self):
        """
        Retrieves all products from the database.

        @return: A list of dictionaries representing the products.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # SQL query to select specific columns from two tables using an INNER JOIN
        query = (
            "SELECT products.product_id, products.name, products.unit_of_measure_id, products.price_per_unit, unit_of_measures.unit_of_measure_name FROM products INNER JOIN unit_of_measures ON products.unit_of_measure_id=unit_of_measures.unit_of_measure_id")
        # Execute the SQL query using the cursor
        cursor.execute(query)
        # Initialize an empty list to store the query response
        response = []
        # Iterate over the result set returned by the query and append each row to the response list as a dictionary
        for (product_id, name, unit_of_measure_id, price_per_unit, unit_of_measure_name) in cursor:
            response.append({
                'product_id': product_id,
                'name': name,
                'unit_of_measure_id': unit_of_measure_id,
                'price_per_unit': price_per_unit,
                'unit_of_measure_name': unit_of_measure_name
            })
        # Return the response list
        return response

    # @contract
    # @pre(lambda product: isinstance(product, dict), "The product must be a dictionary.")
    # @pre(lambda product: 'name' in product and 'unit_of_measure_id' in product and 'price_per_unit' in product,
    # "The product dictionary must contain 'name', 'unit_of_measure_id', and 'price_per_unit' keys.")
    # @post(lambda result: isinstance(result, int), "The return value must be an integer.")
    def insert_new_product(self, product):
        """
        Inserts a new product into the database.

        @param product: A dictionary containing the product information.
        @return: The ID of the inserted product.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # SQL query to insert data into the 'products' table
        query = ("INSERT INTO products "
                 "(name, unit_of_measure_id, price_per_unit)"
                 "VALUES (%s, %s, %s)")
        # Data to be inserted into the table
        data = (product['name'], product['unit_of_measure_id'], product['price_per_unit'])

        # Execute the SQL query with the provided data
        cursor.execute(query, data)
        # Commit the changes to the database
        self.connection.commit()
        # Return the last inserted row ID
        return cursor.lastrowid

    # @contract
    # @pre(lambda product_id: isinstance(product_id, int), "The product_id must be an integer.")
    # @post(lambda result: isinstance(result, bool), "The return value must be an Boolean.")
    def delete_product(self, product_id):
        """
        @ param product_id: The product_id of the product to be deleted.
        @ return result: A boolean value indicate successful deletion of the product.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # Disable foreign key checks
        disable_fk_query = "SET FOREIGN_KEY_CHECKS = 0"
        cursor.execute(disable_fk_query)
        # SQL query to delete specific product from products table
        query = (
            "DELETE FROM products WHERE product_id = %s"
        )
        # Execute the SQL query using the cursor
        cursor.execute(query, (product_id,))
        # Get the affected row count, returns positive number if deleted else return 0 if product with product_id is
        # not found.
        row_count = cursor.rowcount
        result = row_count > 0
        # Disable foreign key checks
        enable_fk_query = "SET FOREIGN_KEY_CHECKS = 1"
        cursor.execute(enable_fk_query)
        # Commit the changes to the database
        self.connection.commit()
        return result

    # @contract
    # @pre(lambda product_id: isinstance(product_id, int), "The product_id must be an integer.")
    # @pre(lambda updated_price: isinstance(updated_price, double), "The product_id must be double.")
    # @post(lambda result: isinstance(result, bool), "The return value must be an Boolean.")
    def update_product_details(self,  product_id, updated_price):
        """
        Update details of product in the database.
        @ param product_id: The ID of the product that must be updated with price details.
        @ param updated_price: The data of the product to be updated.
        @ return: A boolean value indicating whether the update is successful.
        """
        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # SQL query to update price into the 'products' table
        query = (
            "UPDATE products SET price_per_unit = %s WHERE product_id = %s"
        )
        # Execute the SQL query with the provided data
        cursor.execute(query, (updated_price, product_id))
        # Commit the changes to the database
        self.connection.commit()
        # Get the affected row count, returns positive number if updated else return 0 if product with product_id is
        # not found.
        row_count = cursor.rowcount
        # Assign the boolean result
        result = True if row_count > 0 else False
        # Returns True if successful else False
        return result

    # @contract
    # @pre: start_date and end_date must be strings.
    # @post: The return value must be a dictionary containing the total sales report.
    def total_sales(self, start_date, end_date):
        """
        Generate total sales report between the specified dates.

        @param start_date: The start date of the report period.
        @param end_date: The end date of the report period.
        @return response:A list containing the total sales report.
        """
        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # Empty List to hold the final response
        response = []
        # Query to get total sales
        query = (
                "SELECT order_id, customer_name, datetime, total_amount " +
                "FROM orders " +
                "WHERE datetime BETWEEN %s AND %s GROUP BY order_id, customer_name")
        # Execute the query with the start date and end date parameters
        cursor.execute(query, (start_date, end_date))
        # Fetch all the rows from the results set
        results = cursor.fetchall()
        # Create a list of dictionaries representing each order with its details
        response = [{'order_id': row[0], 'customer_name': row[1], 'datetime': row[2], 'total_amount': row[3]} for row in
                    results]
        # Calculate the total sales by summing the total_amount values from the results
        total_sales = sum(row[3] for row in results)
        # Append a dictionary to the response list with the total_sales value
        response.append({'total_sales': total_sales})
        return response

    # @contract
    # @pre: start_date and end_date must be strings.
    # @post: The return value must be a dictionary containing the top selling products.
    def top_selling_products(self, start_date, end_date):
        """
        Generate top selling products between the specified dates.

        @param start_date: The start date of the report period.
        @param end_date: The end date of the report period.
        @return response:A list containing the top selling products.
        """
        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # Empty List to hold the final response
        response = []
        # Query to get top selling products
        query = (
                "SELECT products.product_id, products.name, SUM(order_details.quantity) AS total_quantity " +
                "FROM products " +
                "JOIN order_details ON products.product_id = order_details.product_id " +
                "JOIN orders ON order_details.order_id = orders.order_id " +
                "WHERE orders.datetime BETWEEN %s AND %s " +
                "GROUP BY products.product_id " +
                "ORDER BY total_quantity DESC " +
                "LIMIT 5")

        # Execute the query with the start date and end date parameters
        cursor.execute(query, (start_date, end_date))
        # Fetch all the rows from the results set
        results = cursor.fetchall()
        # Create a list of dictionaries representing the top five selling produts with details
        response = [{'product_id': row[0], 'products_name': row[1], 'total_quantity': row[2]} for row in results]
        # Returns the top selling products as response list
        return response

    # @contract
    # @pre: start_date and end_date must be strings.
    # @post: The return value must be a dictionary containing the sales by category.
    def sales_by_category(self, start_date, end_date):
        """
        Generate sales report by category between the specified dates.

        @param start_date: The start date of the report period.
        @param end_date: The end date of the report period.
        @return response:A list containing the sales report by category.
        """
        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # Empty List to hold the final response
        response = []
        # Query to get sales report by category
        query = (
                "SELECT categories.category_name, SUM(order_details.total_price) AS total_sales" +
                "FROM categories " +
                "JOIN products ON categories.category_id = products.category_id " +
                "JOIN order_details ON products.product_id = order_details.product_id " +
                "JOIN orders ON order_details.order_id = orders.order_id " +
                "WHERE orders.datetime BETWEEN %s AND %s " +
                "GROUP BY categories.category_id " +
                "ORDER BY total_sales DESC"
        )
        # Execute the query with the start date and end date parameters
        cursor.execute(query, (start_date, end_date))
        # Fetch all the rows from the results set
        results = cursor.fetchall()
        # Create a list of dictionaries representing the sales report by category
        response = [{'category_name': row[0], 'total_sales': round(row[1], 2)} for row in results]
        # Returns the sales report by category as response list
        return response
    
    # @contract
    # @pre: product_name must be a string.
    # @post: The return value must be a dictionary representing the product found, or None if not found.
    def search_products(self, product_name):
        """
        Retrieves a specific product from the database based on the provided product name.

        @param product_name: The name of the product to search for.
        @return: A dictionary representing the product, or None if not found.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # SQL query to select specific columns from two tables using an INNER JOIN, with a WHERE clause to filter by product name
        query = (
            "SELECT products.product_id, products.name, products.unit_of_measure_id, products.price_per_unit, unit_of_measures.unit_of_measure_name "
            "FROM products "
            "INNER JOIN unit_of_measures ON products.unit_of_measure_id = unit_of_measures.unit_of_measure_id "
            "WHERE products.name = %s"
        )
        # Execute the SQL query using the cursor, passing the product name as a parameter
        cursor.execute(query, (product_name,))
        # Fetch the first row from the result set
        result = cursor.fetchone()

        # If a result was found, return it as a dictionary; otherwise, return None
        if result:
            product_id, name, unit_of_measure_id, price_per_unit, unit_of_measure_name = result
            return {
                'product_id': product_id,
                'name': name,
                'unit_of_measure_id': unit_of_measure_id,
                'price_per_unit': price_per_unit,
                'unit_of_measure_name': unit_of_measure_name
            }
        else:
            return None





#def main():
#    connection = SQLConnection()
#    connection = connection.connect()

#    products = Products(connection)
#    products.get_all_products()
#     products.insert_new_product({
#         'name': 'potatoes',
#         'unit_of_measure_id': '1',
#         'price_per_unit': 10
#     })

#if __name__ == '__main__':
#    main()
