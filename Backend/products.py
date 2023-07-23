# from contracts import contract, pre, post

""" @ref R6_0"""
# This Class is part of the @ref Model within the overall @ref ModelViewController Design.
# This class implements the methods related to products.
from datetime import date
from typing import Any


class Products:
    def __init__(self, connection) -> None:
        """
        @brief Constructor for the Products class.   
        Initializes an instance of the Products class with the provided database connection object.
        @param connection: The database connection object.
        """
        
        self.connection = connection

    # @contract
    # @post(lambda result: isinstance(result, list), "The return value must be a list.")
    """ @ref R6_0"""
    def get_all_products(self) -> list:
        """
        @brief Retrieves all products from the database.
        This method executes an SQL query to select specific columns from two tables using an INNER JOIN and retrieves all products along with their associated unit of measures from the database.
        @pre The database connection must be established and valid.
        @return A list of dictionaries representing the products. Each dictionary contains product details such as 'product_id', 'name', 'unit_of_measure_id', 'price_per_unit', and 'unit_of_measure_name'.
        @post The response_list is populated with dictionaries representing products, each containing product details.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # SQL query to select specific columns from two tables using an INNER JOIN
        query = (
            "SELECT products.product_id, products.name, products.unit_of_measure_id, products.price_per_unit, unit_of_measures.unit_of_measure_name FROM products INNER JOIN unit_of_measures ON products.unit_of_measure_id=unit_of_measures.unit_of_measure_id")
        # Execute the SQL query using the cursor
        cursor.execute(query)
        # Initialize an empty list to store the query response
        product_list = []
        # Iterate over the result set returned by the query and append each row to the response list as a dictionary
        for (product_id, name, unit_of_measure_id, price_per_unit, unit_of_measure_name) in cursor:
            product_list.append({
                'product_id': product_id,
                'name': name,
                'unit_of_measure_id': unit_of_measure_id,
                'price_per_unit': price_per_unit,
                'unit_of_measure_name': unit_of_measure_name
            })
        # Return the response list
        return product_list

    # @contract
    # @pre(lambda product: isinstance(product, dict), "The product must be a dictionary.")
    # @post(lambda result: isinstance(result, int), "The return value must be an integer.")
    """ @ref R7_0"""
    def insert_new_product(self, product: dict[str, Any]) -> int:
        """
        @brief Inserts a new product into the database.
        This method inserts a new product into the 'products' table of the database using the provided product information.
        @param product: A dictionary containing the product information. The dictionary should have keys 'name', 'unit_of_measure_id', and 'price_per_unit', representing the name of the product, the unit of measure ID, and the price per unit, respectively.
        @pre The database connection must be established and valid.
        @return The ID of the inserted product (last inserted row ID).
        @post The product information is successfully inserted into the 'products' table.
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
    """ @ref R9_0"""
    def delete_product(self, product_id: int) -> bool:
        """
        @brief Deletes a product from the database.
        This method deletes a product from the 'products' table of the database based on the provided product_id.
        @param product_id: The product_id of the product to be deleted.
        @pre The database connection must be established and valid.
        @return A boolean value indicating the successful deletion of the product. Returns True if the product is deleted, and False if the product with the given product_id is not found in the 'products' table.
        @post The product with the specified product_id is deleted from the 'products' table.
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
        # Check if the product was successfully deleted based on the row count
        is_product_deleted = row_count > 0
        # Disable foreign key checks
        enable_fk_query = "SET FOREIGN_KEY_CHECKS = 1"
        cursor.execute(enable_fk_query)
        # Commit the changes to the database
        self.connection.commit()
        return is_product_deleted

    # @contract
    # @pre(lambda product_id: isinstance(product_id, int), "The product_id must be an integer.")
    # @pre(lambda updated_price: isinstance(updated_price, double), "The product_id must be double.")
    # @post(lambda result: isinstance(result, bool), "The return value must be an Boolean.")
    """ @ref R8_0"""
    def update_product_details(self,  product_id: int, updated_price: float) -> bool:
        """
        @brief Update details of a product in the database.
        This method updates the price of a product in the 'products' table of the database based on the provided product_id.
        @param product_id: The ID of the product that must be updated with the updated price details.
        @param updated_price: The new price to be updated for the product.
        @pre The database connection must be established and valid.
        @return A boolean value indicating whether the update is successful. Returns True if the product is updated, and False if the product with the given product_id is not found in the 'products' table or if there are no changes made to the product.
        @post The price of the product with the specified product_id is updated in the 'products' table if the update is successful.
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
        # Assign the boolean result indicating whether the update is successful
        is_update_successful = True if row_count > 0 else False
        # Returns True if successful else False
        return is_update_successful

    # @contract
    # @pre: start_date and end_date must be strings.
    # @post: The return value must be a dictionary containing the total sales report.
    """ @ref R34_0"""
    def total_sales(self, start_date: date, end_date: date) -> list[dict[str, Any]]:
        """
        @brief Generate a total sales report between the specified dates.
        This method generates a total sales report for orders placed between the specified start_date and end_date.
        @param start_date: The start date of the report period.
        @param end_date: The end date of the report period.
        @pre The database connection must be established and valid.
        @return A list containing the total sales report. The list consists of dictionaries, each representing an order with 'order_id', 'customer_name', 'datetime', and 'total_amount' details, and a final entry with 'total_sales' representing the overall total sales amount for the specified period.
        @post The response list is populated with order details and the 'total_sales' value representing the overall total sales amount for the specified period.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # Empty List to hold the final response
        sales_report_list = []
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
        sales_report_list = [{'order_id': row[0], 'customer_name': row[1], 'datetime': row[2], 'total_amount': row[3]} for row in
                    results]
        # Calculate the total sales by summing the total_amount values from the results
        total_sales = sum(row[3] for row in results)
        # Append a dictionary to the response list with the total_sales value
        sales_report_list.append({'total_sales': total_sales})
        return sales_report_list

    # @contract
    # @pre: start_date and end_date must be strings.
    # @post: The return value must be a dictionary containing the top selling products.
    """ @ref R34_0"""
    def top_selling_products(self, start_date: date, end_date: date) -> list[dict[str, Any]]:
        """
        @brief Generate a list of top selling products between the specified dates.
        This method generates a list of top selling products based on the quantity of products sold between the specified start_date and end_date.
        @param start_date: The start date of the report period.
        @param end_date: The end date of the report period.
        @pre The database connection must be established and valid.
        @return A list containing the top selling products. The list consists of dictionaries, each representing a product with 'product_id', 'product_name', and 'total_quantity' details.
        @post The top_selling_products list is populated with the top selling products based on the quantity of products sold between the specified start_date and end_date.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # Empty List to hold the final response
        top_selling_products_list = []
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
        top_selling_products_list = [{'product_id': row[0], 'products_name': row[1], 'total_quantity': row[2]} for row in results]
        # Returns the top selling products as response list
        return top_selling_products_list

    # @contract
    # @pre: start_date and end_date must be strings.
    # @post: The return value must be a dictionary containing the sales by category.
    """ @ref R34_0"""
    def sales_by_category(self, start_date: date, end_date: date) -> list[dict[str, Any]]:
        """
        @brief Generate a sales report by category between the specified dates.
        This method generates a sales report by category based on the total sales (total_price) of products in each category between the specified start_date and end_date.
        @param start_date: The start date of the report period.
        @param end_date: The end date of the report period.
        @pre The database connection must be established and valid.
        @return A list containing the sales report by category. The list consists of dictionaries, each representing a category with 'category_name' and 'total_sales' details.
        @post The sales_by_category list is populated with the sales report by category based on the total sales (total_price) of products in each category between the specified start_date and end_date.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        # Empty List to hold the final response
        sales_by_category_list = []
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
        sales_by_category_list = [{'category_name': row[0], 'total_sales': round(row[1], 2)} for row in results]
        # Returns the sales report by category as response list
        return sales_by_category_list
    
    # @contract
    # @pre: product_name must be a string.
    # @post: The return value must be a dictionary representing the product found, or None if not found.
    """ @ref R10_0"""
    def search_products(self, product_name: str) -> dict[str, Any]:
        """
        @brief Retrieves a specific product from the database based on the provided product name.
        This method searches for a product in the 'products' table of the database with the given product name.
        @param product_name: The name of the product to search for.
        @pre The database connection must be established and valid.
        @return A dictionary representing the product with the provided product_name. Returns None if the product with the given name is not found.
        @post If the product with the specified product_name exists in the 'products' table, the method returns a dictionary containing product details. Otherwise, it returns None.
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
        product_data = cursor.fetchone()
        # return result as a dictionary
        product_id, name, unit_of_measure_id, price_per_unit, unit_of_measure_name = product_data
        return {
            'product_id': product_id,
            'name': name,
            'unit_of_measure_id': unit_of_measure_id,
            'price_per_unit': price_per_unit,
            'unit_of_measure_name': unit_of_measure_name
        }
