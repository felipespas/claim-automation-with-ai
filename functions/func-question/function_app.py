import os
import azure.functions as func
import logging
import json
from utils_lake import *
from utils_openai import *

# storage_account_container_emails = os.environ['STORAGE_ACCOUNT_CONTAINER_EMAILS']
container_name_for_jsons = os.environ['CONTAINER_NAME_FOR_JSONS']

app = func.FunctionApp()

@app.route(route="question01", auth_level=func.AuthLevel.FUNCTION)
def question01(req: func.HttpRequest) -> func.HttpResponse:
    
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
    question = req_body.get('question')

    if directory is None:
        return func.HttpResponse(f'\n Error: Blank directory. Not proceeding with next steps. \n\n', status_code=400)
    if question is None:
        return func.HttpResponse(f'\n Error: Blank question. Not proceeding with next steps. \n\n', status_code=400)

    logging.info(f'Directory: {directory}')

    json_files = list_files(container_name_for_jsons, directory)

    logging.info(f'Json files: {json_files}')

    context = []

    for file in json_files:
        result = download_content(container_name_for_jsons, file)
        context.append(result)

    logging.info(f'Question: {question}')
    logging.info(f'Context: {context}')

    response, tokens = make_question(question, context)   
    
    logging.info(f'Total tokens: {str(tokens)}')
    logging.info(f'Response: {response}')

    return func.HttpResponse(f'\n Resposta: {response} \n\n', status_code=200)
