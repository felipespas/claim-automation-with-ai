import azure.functions as func
import datetime
import json
import logging
from utils_openai import make_question
from utils_lake import get_filepath_from_lake

app = func.FunctionApp()

@app.route(route="validate01", auth_level=func.AuthLevel.FUNCTION)
def validate01(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    question = req_body.get('question')
    json_url = req_body.get('json_url')

    json_sas = get_filepath_from_lake(json_url)

    response = make_question(question)

    return func.HttpResponse(f"Hello, here is your response: {response}!")