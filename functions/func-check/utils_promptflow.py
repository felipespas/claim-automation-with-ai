import os
from dotenv import load_dotenv
from promptflow.client import load_flow
from promptflow.entities import AzureOpenAIConnection

load_dotenv()

open_ai_key = os.environ.get("AZURE_OPENAI_API_KEY")
open_ai_api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
open_ai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
open_ai_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")

def exec_promptflow01(directory:str) -> str:

    open_ai_connection_name = "azure-open-ai-connection"

    connection = AzureOpenAIConnection(
        name=open_ai_connection_name,
        api_key=open_ai_key,
        api_base=open_ai_api_base,
        api_type="azure",
        api_version=open_ai_api_version,
    )

    open_ai_deployment = "gpt-4-0125-preview"

    flow_path = "promptflow/"

    f = load_flow(
        source=flow_path,
    )
    
    # directly use connection created above
    f.context.connections = {"get_order_id": {"connection": connection, "deployment_name": open_ai_deployment},
                            "generate_report_cx": {"connection": connection, "deployment_name": open_ai_deployment},
                            "generate_report_db": {"connection": connection, "deployment_name": open_ai_deployment},
                            "extract_requests": {"connection": connection, "deployment_name": open_ai_deployment},
                            "compare_order_date": {"connection": connection, "deployment_name": open_ai_deployment},
                            "compare_customer_name": {"connection": connection, "deployment_name": open_ai_deployment}
                            }

    result = f(directory=directory)

    result = str(result)

    return result