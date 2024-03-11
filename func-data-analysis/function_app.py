import azure.functions as func
import datetime
import json
import logging
from utils_openai import make_question

app = func.FunctionApp()

@app.route(route="validate01", auth_level=func.AuthLevel.FUNCTION)
def validate01(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    question = req_body.get('question')

    response = make_question(question)

    return func.HttpResponse(f"Hello, here is your response: {response}!")