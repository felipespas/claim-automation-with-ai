import azure.functions as func
import datetime
import json
import logging
from utils_ia import capture_text_from_image, capture_text_from_pdf
from utils_lake import get_filepath_from_lake

app = func.FunctionApp()

@app.route(route="validacaoinicial", auth_level=func.AuthLevel.FUNCTION)
def validacaoinicial(req: func.HttpRequest) -> func.HttpResponse:
    
    # example of image_fullname: "1/Redes de proteção.jpeg"
    # example of pdf_fullname: "1/Pedido 02.pdf"
    
    logging.info('Python HTTP trigger function processed a request.')
    
    req_body = req.get_json()    
    image_path = req_body.get('image_path')
    pdf_path = req_body.get('pdf_path')    

    result = {}

    if image_path:
        image_sas = get_filepath_from_lake(image_path)
        image_json = capture_text_from_image(image_sas)
        result.update({"image": image_json})

    if pdf_path:
        pdf_sas = get_filepath_from_lake(pdf_path)
        pdf_json = capture_text_from_pdf(pdf_sas)
        result.update({"pdf": pdf_json})

    return func.HttpResponse(f"Hello, This HTTP triggered function executed successfully. \n Result: {json.dumps(result)}.")

@app.route(route="validacaocomplementar", auth_level=func.AuthLevel.FUNCTION)
def validacaocomplementar(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )