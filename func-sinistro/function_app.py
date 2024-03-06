import azure.functions as func
import logging
from utils_ia import capture_text_from_image, capture_text_from_pdf
from utils_lake import get_filepath_from_lake, save_json_to_lake
from utils_text import extract_content_from_eml, validate_path

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

    # validate the file path, and if it contains the container name, remove it
    file_path = validate_path(file_path)

    result = {}  

    # capture the file extension based on the file_path
    file_type = file_path.split(".")[-1]   

    if file_type == "jpeg" or file_type == "png" or file_type == "jpg":
        file_sas = get_filepath_from_lake(file_path)
        result_json = capture_text_from_image(file_sas)

    elif file_type == "pdf":        
        file_sas = get_filepath_from_lake(file_path)
        result_json = capture_text_from_pdf(file_sas)

    elif file_type == "eml":
        result_json = extract_content_from_eml(file_path)

    else:
        return func.HttpResponse(
             "Você não forneceu dados em um dos formatos atualmente suportados. Por favor, reveja sua solicitação.",
             status_code=200
        )
    
    result.update({"file_path": file_path})
    result.update({"content": result_json})

    success = save_json_to_lake(result, file_path)

    if success == 0:
        return func.HttpResponse("Dados salvos com sucesso.",status_code=200)