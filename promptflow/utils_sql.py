import os
import pyodbc
import json

sql_conn_str = os.environ["SQL_CONN_STR"]

def query_product_catalog(product_id: int):

    # Create a new connection
    conn = pyodbc.connect(sql_conn_str)

    # Create a new cursor from the connection
    cursor = conn.cursor()

    # Execute the stored procedure
    cursor.execute("{CALL p_ReturnProductData (?)}", product_id)

    # Fetch the JSON document as a string
    json_string = cursor.fetchone()[0]

    # Parse the JSON string into a Python object
    data = json.loads(json_string)

    print(data)

    # Don't forget to close the connection when you're done
    conn.close()

    return data