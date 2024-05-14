import azure.functions as func
import datetime
import json
import logging
from utils_lake import *
from utils_ia import *
from utils_text import *

storage_account_container_emails = os.environ['STORAGE_ACCOUNT_CONTAINER_EMAILS']
storage_account_container_jsons = os.environ['STORAGE_ACCOUNT_CONTAINER_JSONS']
event_hub_name = os.environ['EVENT_HUB_NAME']

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name=event_hub_name,
                               connection="EVENT_HUB_CONN_STR") 
def receive01(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
    
    message = azeventhub.get_body().decode('utf-8')

    try:       
        message_json = json.loads(message)

        directory = message_json.get('directory')

        if directory is None:
            return func.HttpResponse(f'\n Error: Blank directory. Not proceeding with next steps. \n\n', status_code=400)

        data = json.dumps(message_json, indent=4)

        print(data)

        email_files = list_files(storage_account_container_emails, directory)

        logging.info(f'Files listed: {email_files}')

        print(f'Files listed: {email_files}')

        processed_files = []
        format_not_supported_files = []

        for file in email_files:

            logging.info(f'Starting processing: {file}')

            # image
            if file.endswith(".jpeg") or file.endswith(".jpg") or file.endswith(".png"):
                blob_path = get_filepath_from_lake(storage_account_container_emails, file)
                result = capture_text_from_image(blob_path)

            # email
            elif file.endswith(".eml"):
                content = download_content(storage_account_container_emails, file)
                result = extract_content_from_eml(content)
                
            # pdf
            elif file.endswith(".pdf"):
                blob_path = get_filepath_from_lake(storage_account_container_emails, file)
                result = capture_text_from_pdf(blob_path)

            save_json_to_lake(storage_account_container_jsons, file, result)

            logging.info(f'File processed: {file}')

            print(f'File processed: {file}')

            # append file to processed_files
            processed_files.append(file)

        logging.info('All files saved as json and context obtained.\n')

        logging.info(f'\n Processing complete! Files processed: {processed_files}. \n\n Not supported (skipped) files: {format_not_supported_files}\n')

    except Exception as e:
        logging.info("Error: " + str(e))

    