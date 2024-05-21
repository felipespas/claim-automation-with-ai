import os
from promptflow import tool
from utils_lake import *

# read from environment variables
container_name_for_jsons = os.getenv("CONTAINER_NAME_FOR_JSONS")

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(directory: str) -> str:
    
    json_files = list_files(container_name_for_jsons, directory)

    context = []

    for file in json_files:
        result = download_content(container_name_for_jsons, file)
        context.append(result)

    return context