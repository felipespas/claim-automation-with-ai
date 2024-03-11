import os
import logging
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

    # decode the content
    downloaded_content = downloaded_content.decode("utf-8")

    return downloaded_content

def list_files(dir_path):
    logging.info('Initializing client.')
    
    # Create a DataLakeServiceClient object
    service_client = DataLakeServiceClient(account_url=storage_account_url, credential=storage_account_key)

    # Get the file system client
    file_system_client = service_client.get_file_system_client(json_container_name)

    # Get the directory client
    directory_client = file_system_client.get_paths(dir_path)    

    logging.info('Client instantiated. Starting loop.')

    # iterate over the files and store their names in a list
    file_list = []
    
    for file in directory_client:
        file_name_str = file.name
        logging.info(f'File found: {file_name_str}')
        file_list.append(file.name)    

    logging.info('Loop finished. Returning file_list.')

    return file_list