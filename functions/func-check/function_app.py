import azure.functions as func
import datetime
import json
import logging
from utils_promptflow import *

app = func.FunctionApp()

@app.route(route="check01", auth_level=func.AuthLevel.FUNCTION)
def check01(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    logging.info('This was the payload sent: ' + str(req_body))

    # check if the request body is string and convert it to json
    try:        
        if isinstance(req_body, str):
            req_body = json.loads(req_body)            
            logging.info('Payload correctly converted to JSON')
    except:
        logging.info(f'Error when processing the following input: {req_body}')
        return func.HttpResponse(f'\n Error: invalid JSON. Not proceeding with next steps. \n\n', status_code=400)
    
    directory = req_body.get('directory')    

    logging.info('Invoking exec_promptflow function.')

    result = exec_promptflow01(directory)    

    logging.info(f'This is the result: {result}')

    return func.HttpResponse(f"\n Result: {result}", status_code=200)