import azure.functions as func
import datetime
import json
import logging
from utils_eventhub import *

app = func.FunctionApp()

@app.route(route="receive01", auth_level=func.AuthLevel.FUNCTION)
def receive01(req: func.HttpRequest) -> func.HttpResponse:

    logging.info(f'Starting execution with the following payload: {req.get_json()}.')

    req_body = req.get_json()    
    
    try:
        event_data_json = json.dumps(req_body)    
        event_data_str = str(event_data_json)

    except Exception as e:
        logging.info(f'Error when processing the following input: {req_body}. Error: {str(e)}')
        return func.HttpResponse(f'\n Error: Data provided is not a valid JSON. \n\n', status_code=400)

    try:        
        asyncio.run(send_event(event_data_str)) 
    
        logging.info(f'Data sent to partition: {event_data_str}.')

        logging.info(f'Returning http status 202 to the caller application.')

        return func.HttpResponse(
            "This wrapper HTTP triggered function was executed successfully. Returning status code 202.\n",
            status_code=202
        )    
    
    except Exception as e:
        logging.info(f'Error when processing the following input: {req_body}. Error: {str(e)}')
        return func.HttpResponse(f'\n Error: Error when sending data to Event Hub. \n\n', status_code=400)