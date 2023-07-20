# from contracts import contract, pre, post

""" @ref R71"""
class unit_of_measures:
    def __init__(self, connection):
        """
        Constructor for unit_of_measures class.

        @param connection: The database connection object.
        """
        self.connection = connection

    # @contract
    # @post(lambda result: isinstance(result, list), "The return value must be a list.")
    def get_unit_of_measures(self):
        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor() 
        # SQL query to retrieve unit of measures 
        query = ("SELECT * FROM unit_of_measures") 
        # Execute the query using the cursor
        cursor.execute(query)  
        response = []
        # Iterate over the query results
        for unit_of_measure_id, unit_of_measure_name in cursor:  
            # Create a dictionary for each unit of measure
            response.append({  
                # Store the unit_of_measure_id
                'unit_of_measure_id': unit_of_measure_id,  
                # Store the unit_of_measure_name
                'unit_of_measure_name': unit_of_measure_name  
            })
        # Return the list of unit of measures dictionaries
        return response
