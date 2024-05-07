import azure.functions as func
import datetime
import json
import logging
from utils_eventhub import *

app = func.FunctionApp()

@app.route(route="wrapper01", auth_level=func.AuthLevel.FUNCTION)
def wrapper01(req: func.HttpRequest) -> func.HttpResponse:

    req_body = req.get_json()
    
    try:
        data = str(req_body)
        
        asyncio.run(send_event(data)) 
        
        logging.info(f'Data sent to partition.')

        return func.HttpResponse(
            "This wrapper HTTP triggered function was executed successfully. Returning status code 202.\n",
            status_code=202
        )    
    
    except Exception as e:
        
        # show the raw error message
        logging.info(f'Error when processing the following input: {req_body}. Error: {str(e)}')
        

    #     logging.info(f'Error when processing the following input: {req_body}')
    #     return func.HttpResponse(f'\n Error: Not proceeding with next steps. \n\n', status_code=400)