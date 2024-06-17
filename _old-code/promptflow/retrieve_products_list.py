
from promptflow.core import tool
from utils_sql import *


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(order_id: str) -> str:
    
    # result = query_order_products_names(order_id)

    result = query_order_product_details(order_id)

    return str(result)
