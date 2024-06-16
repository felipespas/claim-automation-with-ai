# create needed connection
# import promptflow
from promptflow.client import load_flow
from promptflow.entities import AzureOpenAIConnection

conn_name = "openai1704eastus"
api_key = "9109fbe161b74eb8be93799a0954a230"
api_base = "https://openai1704eastus.openai.azure.com/"
api_version = "2024-02-01"

# Follow https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal to create an Azure Open AI resource.
connection = AzureOpenAIConnection(
    name=conn_name,
    api_key=api_key,
    api_base=api_base,
    api_type="azure",
    api_version=api_version,
)

deployment_name = "gpt-4-0125-preview"

flow_path = "."
directory = "638530437990000000"

f = load_flow(
    source=flow_path,
)
# directly use connection created above
f.context.connections = {"get_order_id": {"connection": connection, "deployment_name": deployment_name},
                         "generate_report_cx": {"connection": connection, "deployment_name": deployment_name},
                         "generate_report_db": {"connection": connection, "deployment_name": deployment_name},
                         "extract_requests": {"connection": connection, "deployment_name": deployment_name},
                         "compare_order_date": {"connection": connection, "deployment_name": deployment_name},
                         "compare_customer_name": {"connection": connection, "deployment_name": deployment_name}
                         }

result = f(directory=directory)

print(result)