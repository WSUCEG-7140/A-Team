import mysql.connector

class SQLConnection:
    def __init__(self):
        self.connection = None

    def connect(self, user, password, database):
        if self.connection is None:
            self.connection = mysql.connector.connect(user=user, password=password, database=database)
        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None


