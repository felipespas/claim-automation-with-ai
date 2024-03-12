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

@app.route(route="processor01", auth_level=func.AuthLevel.FUNCTION)
def processor01(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    directory = req_body.get('directory')
    question = req_body.get('question')

    email_files = list_files(storage_account_container_emails, directory)

    context = []

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
        
        context.append(result)

    logging.info('All files saved as json and context obtained.\n')

    response = make_question(question, context)        

    return func.HttpResponse(f'\n Processamento OK! \n Resposta à pergunta do usuário: {response} \n\n', status_code=200)

