import azure.functions as func
import datetime
import json
import logging
from utils_ia import capture_text_from_image
from utils_lake import get_filepath_from_lake

app = func.FunctionApp()

@app.route(route="validacaoinicial", auth_level=func.AuthLevel.FUNCTION)
def validacaoinicial(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    blobpath = req.params.get('blobpath')
    if not blobpath:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            blobpath = req_body.get('blobpath')

    blob_sas = get_filepath_from_lake(blobpath)
    result_json = capture_text_from_image(blob_sas)

    if result_json:
        return func.HttpResponse(f"Hello, This HTTP triggered function executed successfully. Result: {result_json}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

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