import os
import pyodbc
import json
import logging
from dotenv import load_dotenv

load_dotenv()

sql_conn_str = os.environ["SQL_CONN_STR"]

def query_order_product_details(order_id: int):

    logging.info(f"Starting function to query order product details for order_id: {order_id}")

    try:
    
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

        logging.info(f"Query successful for order_id: {order_id}")
    
    except Exception as e:

        print(f"Error: {e}")

        logging.error(f"Error at communcating with SQL Server")
        logging.error(f"Error message: {e}")     

    # Parse the JSON string into a Python object        
    try:        

        logging.info(f"Converting JSON string to Python object for order_id: {order_id}")

        data = json.loads(results)
        
        return str(data)
        
    except Exception as e:

        print(f"Error: {e}")

        logging.error(f"Error at converting JSON string to Python object")
        logging.error(f"Error message: {e}")

        

