from sql_connection import SQLConnection
# from contracts import contract, pre, post

class unit_of_measure:
    def __init__(self, connection):
        """
        Constructor for Products class.

        @param connection: The database connection object.
        """
        self.connection = connection

def get_uoms(connection):
    cursor = connection.cursor()
    query = "SELECT uom_id, uom_name FROM uom"
    cursor.execute(query)
    response = []
    for uom_id, uom_name in cursor:
        response.append({
            'uom_id': uom_id,
            'uom_name': uom_name
        })
    return response

#if __name__ == '__main__':
    #from sql_connection import SQLConnection

