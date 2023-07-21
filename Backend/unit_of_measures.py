#from contracts import contract, post

""" @ref R71_0"""
# This Class is part of the @ref Model within the overall @ref ModelViewController Design.
# This class implements the methods related to unit of measures.
class UnitOfMeasures:
    def __init__(self, connection):
        """
        @brief Constructor for the UnitOfMeasures class.   
        Initializes an instance of the UnitOfMeasures class with the provided database connection object.
        @param connection: The database connection object.
        """

        self.connection = connection

    #@contract
    #@post(lambda result: isinstance(result, list), "The return value must be a list.")
    """ @ref R71_0"""
    def get_unit_of_measures(self):
        """
        @brief Retrieves a list of unit of measures from the database.
        This method executes an SQL query to retrieve all unit of measures from the database table "unit_of_measures".
        @return A list of dictionaries containing unit_of_measure_id and unit_of_measure_name for each unit of measure.
        @post The response list is populated with dictionaries representing unit of measures, each containing 'unit_of_measure_id' and 'unit_of_measure_name'.
        """

        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor() 
        # SQL query to retrieve unit of measures 
        query = ("SELECT * FROM unit_of_measures") 
        # Execute the query using the cursor
        cursor.execute(query)  
        unit_of_measures_list = []
        # Iterate over the query results
        for unit_of_measure_id, unit_of_measure_name in cursor:  
            # Create a dictionary for each unit of measure
            unit_of_measures_list.append({  
                # Store the unit_of_measure_id
                'unit_of_measure_id': unit_of_measure_id,  
                # Store the unit_of_measure_name
                'unit_of_measure_name': unit_of_measure_name  
            })
        # Return the list of unit of measures dictionaries
        return unit_of_measures_list
