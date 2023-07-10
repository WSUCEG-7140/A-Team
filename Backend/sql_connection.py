import mysql.connector
#from contracts import contract, pre, post

class SQLConnection:
    def __init__(self):
        self.connection = None

    #@contract
    #@pre(lambda self: self.connection is None, "Connection must not be already established.")
    #@post(lambda self, result: self.connection is not None and result is self.connection,
        # "Connection must be established and returned.")
    def connect(self):
        """
        Connects to the MySQL database.

        @return The MySQL connection object.
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
        Closes the MySQL connection.
        """
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # @contract
    # @post(lambda result: isinstance(result, mysql.connector.cursor.MySQLCursor),
    #       "The return value must be a MySQLCursor object.")
    def cursor(self):
        """
        Returns the cursor object to execute SQL queries
        @ return: The cursor object
        """
        if self.connection is None:
            self.connect()
        return self.connection.cursor()
