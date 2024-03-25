import os
import azure.functions as func
import logging
import json
from utils_lake import list_files, get_filepath_from_lake, save_json_to_lake, download_content
from utils_ia import capture_text_from_pdf_or_image, capture_text_from_office
from utils_text import extract_content_from_eml
from utils_openai import make_question

storage_account_container_emails = os.environ['STORAGE_ACCOUNT_CONTAINER_EMAILS']
storage_account_container_jsons = os.environ['STORAGE_ACCOUNT_CONTAINER_JSONS']

app = func.FunctionApp()

@app.route(route="prepare01", auth_level=func.AuthLevel.FUNCTION)
def prepare01(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    # check if the request body is string and convert it to json
    try:        
        if isinstance(req_body, str):
            req_body = json.loads(req_body)
    except:
        logging.info(f'Error when processing the following input: {req_body}')
        return func.HttpResponse(f'\n Error: invalid JSON. Not proceeding with next steps. \n\n', status_code=400)
    
    directory = req_body.get('directory')

    if directory is None:
        return func.HttpResponse(f'\n Error: Blank directory. Not proceeding with next steps. \n\n', status_code=400)

    email_files = list_files(storage_account_container_emails, directory)

    logging.info(f'Files listed: {email_files}')

    processed_files = []
    format_not_supported_files = []

    # iterate over the files and call a function
    for file in email_files:

        logging.info(f'Starting processing: {file}')

        # pdf or jpeg
        if file.endswith(".pdf") or file.endswith(".jpeg") or file.endswith(".jpg"):
            blob_path = get_filepath_from_lake(storage_account_container_emails, file)
            result = capture_text_from_pdf_or_image(blob_path)
            
        # email
        elif file.endswith(".eml"):
            content = download_content(storage_account_container_emails, file)
            result = extract_content_from_eml(content)
            
        # office files
        elif file.endswith(".docx") or file.endswith(".xlsx") or file.endswith(".pptx"):
        # or file.endswith(".doc") or file.endswith(".xls") or file.endswith(".ppt"):
            
            blob_path = get_filepath_from_lake(storage_account_container_emails, file)
            result = capture_text_from_office(blob_path)          

        else:
            format_not_supported_files.append(file)
            continue

        save_json_to_lake(storage_account_container_jsons, file, result)

        logging.info(f'File processed: {file}')

        # append file to processed_files
        processed_files.append(file)

    logging.info('All files saved as json and context obtained.\n')

    return func.HttpResponse(f'\n Processamento OK! Arquivos processados: {processed_files}. \n\n Arquivos não suportados: {format_not_supported_files}\n\n', status_code=200)

@app.route(route="validate01", auth_level=func.AuthLevel.FUNCTION)
def validate01(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    # check if the request body is string and convert it to json
    try:        
        if isinstance(req_body, str):
            req_body = json.loads(req_body)
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