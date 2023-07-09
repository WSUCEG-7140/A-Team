from sql_connection import SQLConnection
# from contracts import contract, pre, post

class unit_of_measure:
    def __init__(self, connection):
        """
        Constructor for unit_of_measure class.

        @param connection: The database connection object.
        """
        self.connection = connection

# @contract
# @post(lambda result: isinstance(result, list), "The return value must be a list.")
def get_unit_of_measure(connection):
    # Create a cursor object to execute SQL queries
    cursor = connection.cursor() 
    # SQL query to retrieve unit of measure 
    query = "SELECT uom_id, uom_name FROM uom"  
    # Execute the query using the cursor
    cursor.execute(query)  
    response = []
    # Iterate over the query results
    for uom_id, uom_name in cursor:  
        # Create a dictionary for each unit of measure
        response.append({  
            # Store the uom_id
            'uom_id': uom_id,  
            # Store the uom_name
            'uom_name': uom_name  
        })
    # Return the list of unit of measure dictionaries
    return response  

#if __name__ == '__main__':
    #from sql_connection import SQLConnection

