import os
import json
import extract_msg
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.storage.filedatalake import DataLakeServiceClient
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas, BlobClient

load_dotenv()

connection_string = os.environ["STORAGE_CONNECTION_STRING"]
files_container_name = os.environ["STORAGE_CONTAINER_FILES"]
jsons_container_name = os.environ["STORAGE_CONTAINER_JSONS"]
storage_account_key = os.environ["STORAGE_ACCOUNT_KEY"]
storage_account_url = os.environ["DATA_LAKE_URL_ENDPOINT"]

def get_filepath_from_lake(blob_path: str):

    # Create a blob client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(files_container_name, blob_path)

    # Define the expiry time (1 hour from now in this example)
    expiry_time = datetime.utcnow() + timedelta(hours=1)

    # Generate SAS token
    sas_token = generate_blob_sas(
        blob_service_client.account_name,
        files_container_name,
        blob_path,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry_time
    )

    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{files_container_name}/{blob_path}?{sas_token}"

    return blob_url

def save_json_to_lake(json_data, file_path):

    try:

        file_path = file_path + ".json"

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(jsons_container_name, file_path)

        json_str = json.dumps(json_data, ensure_ascii=False).encode('utf-8')

        blob_client.upload_blob(json_str, overwrite=True)

        return 0

    except Exception as e:
        return e        
    
def extract_content_from_msg(file_path):
    
    local_file_path = 'temp.msg'

    # Create a DataLakeServiceClient object
    service_client = DataLakeServiceClient(account_url=storage_account_url, credential=storage_account_key)

    # Get the file system client
    file_system_client = service_client.get_file_system_client(files_container_name)

    # Get the data lake file client
    file_client = file_system_client.get_file_client(file_path)

    # Download the file to a local file
    with open(local_file_path, "wb") as my_blob:
        download_stream = file_client.download_file()
        my_blob.write(download_stream.readall())
    
    msg = extract_msg.Message(local_file_path)

    subject = msg.subject
    body = msg.body.replace('\n', ' ').replace('\r', '')
    sender = msg.sender
    to = msg.to
    cc = msg.cc
    bcc = msg.bcc
    date = msg.date
    attachments = msg.attachments

    result_json = {
        "subject": subject,
        "body": body,
        "sender": sender,
        "to": to,
        "cc": cc,
        "bcc": bcc,
        "date": date.strftime("%Y-%m-%d %H:%M:%S"),
        "attachments": [attachment.longFilename for attachment in attachments]
    }

    # release the lock in the file so I can delete it
    msg.close()

    # delete the file
    os.remove(local_file_path)    

    return result_json

def validate_path(text: str) -> str:    
    # check if the first character is a slash and remove it
    if text[0] == "/":
        text = text[1:]

    # check if the first "folder" is the container
    container_name = text.split("/")[0]
    if container_name == files_container_name:
        text = text.replace(container_name + "/", "")

    return text