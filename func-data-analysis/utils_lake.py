import os
from dotenv import load_dotenv
from azure.storage.filedatalake import DataLakeServiceClient

load_dotenv()

json_container_name = os.environ["STORAGE_CONTAINER_JSONS"]
storage_account_key = os.environ["STORAGE_ACCOUNT_KEY"]
storage_account_url = os.environ["DATA_LAKE_URL_ENDPOINT"]

def download_content(file_path):
    
    # Create a DataLakeServiceClient object
    service_client = DataLakeServiceClient(account_url=storage_account_url, credential=storage_account_key)

    # Get the file system client
    file_system_client = service_client.get_file_system_client(json_container_name)

    # Get the data lake file client
    file_client = file_system_client.get_file_client(file_path)

    # Download the content of the file into a variable
    download_stream = file_client.download_file()
    downloaded_content = download_stream.readall()

    return downloaded_content