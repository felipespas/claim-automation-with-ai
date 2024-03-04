import azure.functions as func
import datetime
import json
import logging
from utils_ia import capture_text_from_image, capture_text_from_pdf
from utils_lake import get_filepath_from_lake
from utils_text import remove_html

app = func.FunctionApp()

@app.route(route="validacaoinicial", auth_level=func.AuthLevel.FUNCTION)
def validacaoinicial(req: func.HttpRequest) -> func.HttpResponse:
    
    # example of image_fullname: "1/Redes de proteção.jpeg"
    # example of pdf_fullname: "1/Pedido 02.pdf"
    
    logging.info('Python HTTP trigger function processed a request.')
    
    req_body = req.get_json()    
    file_path = req_body.get('file_path')
    file_type = req_body.get('file_type')    

    result = {}

    if file_type == "image":
        image_sas = get_filepath_from_lake(file_path)
        image_json = capture_text_from_image(image_sas)
        result.update({"image": image_json})

    elif file_type == "pdf":
        pdf_sas = get_filepath_from_lake(file_path)
        pdf_json = capture_text_from_pdf(pdf_sas)
        result.update({"pdf": pdf_json})

    else:
        return func.HttpResponse(
             "There was an error processing your request. We only support PDF and Images at this moment.",
             status_code=200
        )

    return func.HttpResponse(f"Hello, This HTTP triggered function executed successfully. \n Result: {json.dumps(result)}.")

@app.route(route="removehtml", auth_level=func.AuthLevel.FUNCTION)
def removehtml(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    try:     
        req_body = req.get_json()
        text = req_body.get('text')
        cleaned_text = remove_html(text)

    except Exception as e:
        return func.HttpResponse(
             "There was an error processing your request. Please check your input. The error was: " + str(e),
             status_code=200
        )

    if cleaned_text:
        return func.HttpResponse(cleaned_text)
    else:
        return func.HttpResponse(
             "There is no text inside your html content. Please check your input.",
             status_code=200
        )