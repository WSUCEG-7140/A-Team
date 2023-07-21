import mysql.connector
#from contracts import contract, pre, post

""" @ref R1_0"""
# This Class is part of the @ref Model within the overall @ref ModelViewController Design.
# This Class implements methods for managing a MySQL database connection, including connecting, closing, and retrieving a cursor object for executing SQL queries.
class SQLConnection:
    def __init__(self):
        self.connection = None

    #@contract
    #@pre(lambda self: self.connection is None, "Connection must not be already established.")
    #@post(lambda self, result: self.connection is not None and result is self.connection,
        # "Connection must be established and returned.")
    def connect(self):
        """
        @brief Establishes a connection to the MySQL database using the provided credentials.
        @pre The database connection must not be established or must be closed.
        @return The MySQL connection object.
        @post The database connection is established and open, and the returned connection object is valid.
        """

        user = 'root'  # Set your MySQL username here
        password = 'root'   # Set your MySQL password here
        database = 'grocery_store'  # Set the name of your database here
        if self.connection is None:
            self.connection = mysql.connector.connect(user=user, password=password, database=database)
        return self.connection

    #@contract
    #@pre(lambda self: self.connection is not None, "Connection must be established.")
    #@post(lambda self: self.connection is None, "Connection must be closed.")
    def close(self):
        """
        @brief Closes the existing MySQL connection if it is open. 
        @pre The database connection must be established and open.
        @post The database connection is closed and set to None.
        """

        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # @contract
    # @post(lambda result: isinstance(result, mysql.connector.cursor.MySQLCursor),
    #       "The return value must be a MySQLCursor object.")
    def cursor(self):
        """
        @brief Returns the cursor object to execute SQL queries.
        If the connection is not established, this method first establishes the connection.
        @pre The database connection must be established or valid.
        @return The cursor object to execute SQL queries.
        @post The method returns a valid cursor object.
        @post The database connection is established and can be used to execute queries.
        """

        if self.connection is None:
            self.connect()
        return self.connection.cursor()
