import os
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult, DocumentAnalysisFeature

load_dotenv()

endpoint = os.environ["AISERVICES_ENDPOINT"]
key = os.environ["AISERVICES_KEY"]

def capture_text_from_pdf(blob_url: str):

    client = DocumentAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)     
    )

    poller = client.begin_analyze_document_from_url("prebuilt-document", blob_url)
    result = poller.result()
    
    form_fields = {}
    try:
        if result.content:
            content = result.content.replace("\n", " ")
        
        for pair in result.key_value_pairs:

            if pair.key and pair.key.content:
                key_content = pair.key.content.replace("\n", "\\n").replace("/", "\/")
                    
            if pair.value and pair.value.content:
                value_content = pair.value.content.replace("\n", "\\n").replace("/", "\/")
            else:
                value_content = ""

            # add to form_fields json
            form_fields.update({key_content : value_content})       

        # get data from tables present in the pdf
        headers = []
        row_json = {}
        table_json = {}
        tables_array = []
        for table in result.tables:
            for cell in table.cells:
                row_index = cell.row_index
                if cell.row_index == 0:
                    # append cell content to headers list
                    headers.append(cell.content)
                else:
                    item_json = {headers[cell.column_index] : cell.content}
                    row_json.update(item_json)
                    if cell.column_index == len(headers) - 1:
                        table_json.update({row_index : row_json})
                        row_json = {}
            tables_array.append(table_json)
        
    except Exception as e:
        print(str(e))

    # create a single json with all the data
    result_json = {
        "content": content,
        "fields": form_fields,
        "tables": tables_array
    }

    return result_json

def capture_text_from_office(blob_url: str):

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout", 
        AnalyzeDocumentRequest(url_source=blob_url)
    )

    result: AnalyzeResult = poller.result()

    result_json = {
        "content": result.content.replace("\n", " ")
    }

    return result_json
    