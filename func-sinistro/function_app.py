import os
import azure.functions as func
import logging
from utils_lake import list_files, get_filepath_from_lake, save_json_to_lake, download_content
from utils_ia import capture_text_from_pdf
from utils_text import extract_content_from_eml
from utils_openai import make_question

storage_account_container_emails = os.environ['STORAGE_ACCOUNT_CONTAINER_EMAILS']
storage_account_container_jsons = os.environ['STORAGE_ACCOUNT_CONTAINER_JSONS']

app = func.FunctionApp()

@app.route(route="prepare01", auth_level=func.AuthLevel.FUNCTION)
def prepare01(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    directory = req_body.get('directory')

    email_files = list_files(storage_account_container_emails, directory)

    # iterate over the files and call a function
    for file in email_files:
        if file.endswith(".pdf"):
            blob_path = get_filepath_from_lake(storage_account_container_emails, file)
            result = capture_text_from_pdf(blob_path)
            
        elif file.endswith(".eml"):
            content = download_content(storage_account_container_emails, file)
            result = extract_content_from_eml(content)
            
        else:
            continue

        save_json_to_lake(storage_account_container_jsons, file, result)  

    logging.info('All files saved as json and context obtained.\n')

    return func.HttpResponse(f'\n Processamento OK! Arquivos processados: {email_files}. \n\n', status_code=200)

@app.route(route="validate01", auth_level=func.AuthLevel.FUNCTION)
def validate01(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    directory = req_body.get('directory')
    question = req_body.get('question')

    logging.info(f'Directory: {directory}')

    json_files = list_files(storage_account_container_jsons, directory)

    logging.info(f'Json files: {json_files}')

    context = []

    for file in json_files:
        result = download_content(storage_account_container_jsons, file)
        context.append(result)

    logging.info(f'Question: {question}')
    logging.info(f'Context: {context}')

    response, tokens = make_question(question, context)   
    
    logging.info(f'Total tokens: {str(tokens)}')
    logging.info(f'Response: {response}')

    return func.HttpResponse(f'\n Resposta: {response} \n\n', status_code=200)