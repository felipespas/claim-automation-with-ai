import azure.functions as func
import datetime
import json
import logging
from utils_openai import make_question
from utils_lake import download_content, list_files

app = func.FunctionApp()

@app.route(route="processor01", auth_level=func.AuthLevel.FUNCTION)
def processor01(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    
    question = req_body.get('question')
    logging.info(f'Question received: {question}')

    directory = req_body.get('directory')
    logging.info(f'Directory received: {directory}')

    file_list = list_files(directory)
    logging.info('Files listed.')

    full_content = []
    # iterate over file list and download every doc content
    for file in file_list:
        file_content = download_content(file)

        # convert the content to a json format
        file_json = json.dumps(file_content)

        file_details = {
            "file_name": file,
            "content": file_json
        }

        full_content.append(file_details)

    logging.info('All files content downloaded.\n')

    # save the content in a json file
    with open(f"temp.json", "w") as f:
        json.dump(full_content, f)
    
    logging.info('File saved.\n')

    response = make_question(question, full_content)

    logging.info('Open AI\'s response answered.\n')

    return func.HttpResponse(f"Resposta: {response}\n")