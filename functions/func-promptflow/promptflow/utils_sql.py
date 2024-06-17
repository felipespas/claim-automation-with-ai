import os
import pyodbc
import json
from dotenv import load_dotenv

load_dotenv()

sql_conn_str = os.environ["SQL_CONN_STR"]

def query_order_product_details(order_id: int):

    # Create a new connection
    conn = pyodbc.connect(sql_conn_str)

    # Create a new cursor from the connection
    cursor = conn.cursor()

    # Execute the stored procedure
    cursor.execute("{CALL p_ReturnOrderDetails_JSON (?)}", order_id)

    # If the stored procedure returns results, fetch them
    results = cursor.fetchall()

    # Don't forget to close the connection when you're done
    conn.close()

    results = results[0][0]

    # Parse the JSON string into a Python object        
    try:        
        data = json.loads(results)
        return str(data)
        
    except Exception as e:

        # # write the data to a file
        # with open('_error.txt', 'w') as f:
        #     f.write(results)

        print(f"Error: {e}")

