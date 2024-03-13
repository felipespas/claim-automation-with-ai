
from promptflow import tool
from utils_lake import *

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(directory: str) -> str:
    
    storage_account_container_jsons = "json"
    json_files = list_files(storage_account_container_jsons, directory)

    context = []

    for file in json_files:
        result = download_content(storage_account_container_jsons, file)
        context.append(result)

    return context