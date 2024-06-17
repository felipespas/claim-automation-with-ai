import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from azure.storage.filedatalake import DataLakeServiceClient
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas

load_dotenv()

data_lake_name = os.environ["DATA_LAKE_NAME"]
data_lake_key = os.environ["DATA_LAKE_KEY"]

data_lake_url_endpoint = f"https://{data_lake_name}.dfs.core.windows.net/"
storage_account_connection_string = f"DefaultEndpointsProtocol=https;AccountName={data_lake_name};AccountKey={data_lake_key};EndpointSuffix=core.windows.net"

# Create a blob client
blob_service_client = BlobServiceClient.from_connection_string(storage_account_connection_string)

def list_files(container_name, dir_path):
    
    # Create a DataLakeServiceClient object
    service_client = DataLakeServiceClient(account_url=data_lake_url_endpoint, credential=data_lake_key)

    # Get the file system client
    file_system_client = service_client.get_file_system_client(container_name)

    # Get the directory client
    directory_client = file_system_client.get_paths(dir_path)    

    # iterate over the files and store their names in a list
    file_list = []
    
    for file in directory_client:
        file_list.append(file.name)    

    return file_list
    
def download_content(container, file_path):
    
    # Create a DataLakeServiceClient object
    service_client = DataLakeServiceClient(account_url=data_lake_url_endpoint, credential=data_lake_key)

    # Get the file system client
    file_system_client = service_client.get_file_system_client(container)

    # Get the data lake file client
    file_client = file_system_client.get_file_client(file_path)

    # Download the content of the file into a variable
    download_stream = file_client.download_file()
    downloaded_content = download_stream.readall()

    return downloaded_content