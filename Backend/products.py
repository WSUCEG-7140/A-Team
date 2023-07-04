#from sql_connection import SQLConnection
#from contracts import contract, pre, post

class Products:
    def __init__(self, connection):
        """
        Constructor for Products class.

        @param connection: The database connection object.
        """
        self.connection = connection

    #@contract
    #@post(lambda result: isinstance(result, list), "The return value must be a list.")
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
    
    #@contract
    #@pre(lambda product: isinstance(product, dict), "The product must be a dictionary.")
    #@pre(lambda product: 'name' in product and 'unit_of_measure_id' in product and 'price_per_unit' in product,
     #    "The product dictionary must contain 'name', 'unit_of_measure_id', and 'price_per_unit' keys.")
    #@post(lambda result: isinstance(result, int), "The return value must be an integer.")
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

# def main():
#     connection = SQLConnection()
#     connection = connection.connect()

#     products = Products(connection)
#     products.get_all_products()
#     products.insert_new_product({
#         'name': 'potatoes',
#         'unit_of_measure_id': '1',
#         'price_per_unit': 10
#     })

# if __name__ == '__main__':
#     main()







