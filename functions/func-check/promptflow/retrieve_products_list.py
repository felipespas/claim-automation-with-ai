import logging
from promptflow.core import tool
from utils_sql import *


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(order_id: str) -> str:
    
    logging.info("Retrieve_products_list tool started")

    result = query_order_product_details(order_id)

    logging.info("Retrieve_products_list tool finished successfully")

    return str(result)
