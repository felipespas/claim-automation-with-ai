import azure.functions as func
import datetime
import json
import logging
from utils_ia import capture_text_from_image, capture_text_from_pdf
from utils_lake import get_filepath_from_lake, save_json_to_lake
from utils_text import remove_html, validate_path

app = func.FunctionApp()

@app.route(route="gettext", auth_level=func.AuthLevel.FUNCTION)
def gettext(req: func.HttpRequest) -> func.HttpResponse:
    
    # example of image_fullname: "1/Redes de proteção.jpeg"
    # example of pdf_fullname: "1/Pedido 02.pdf"
    
    logging.info('Python HTTP trigger function processed a request.')
    
    # capture the body of the request
    req_body = req.get_json()    
    
    # capture the file path from the request body
    file_path = req_body.get('file_path')

    # capture the file extension based on the file_path
    file_type = file_path.split(".")[-1]

    # validate the file path, and if it contains the container name, remove it
    file_path = validate_path(file_path)

    result = {}

    if file_type == "jpeg" or file_type == "png" or file_type == "jpg":
        image_sas = get_filepath_from_lake(file_path)
        image_json = capture_text_from_image(image_sas)
        result.update({"image": image_json})

    elif file_type == "pdf":
        pdf_sas = get_filepath_from_lake(file_path)
        pdf_json = capture_text_from_pdf(pdf_sas)
        result.update({"pdf": pdf_json})

    else:
        return func.HttpResponse(
             "There was an error processing your request. Please review the data provided.",
             status_code=200
        )

    success = save_json_to_lake(result, file_path)

    if success == 0:
        return func.HttpResponse("Dados salvos com sucesso.",
             status_code=200
        )

@app.route(route="removehtml", auth_level=func.AuthLevel.FUNCTION)
def removehtml(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    try: 
        result = {}    
        req_body = req.get_json()
        text = req_body.get('text')
        result_text = remove_html(text)
        result.update({"text": result_text})       

    except Exception as e:
        return func.HttpResponse(
             "There was an error processing your request. Please check your input. The error was: " + str(e),
             status_code=200
        )

    if result:
        return func.HttpResponse(f"{json.dumps(result)}.")
    else:
        return func.HttpResponse(
             "There is no text inside your html content. Please check your input.",
             status_code=200
        )