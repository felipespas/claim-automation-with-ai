import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas

load_dotenv()

def get_filepath_from_lake(blob_fullname: str):

    # example of blob_fullname: "1/Redes de proteção.jpeg"

    connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    container_name = os.environ["STORAGE_CONTAINER_NAME"]

    # Create a blob client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container_name, blob_fullname)

    # Define the expiry time (1 hour from now in this example)
    expiry_time = datetime.utcnow() + timedelta(hours=1)

    # Generate SAS token
    sas_token = generate_blob_sas(
        blob_service_client.account_name,
        container_name,
        blob_fullname,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry_time
    )

    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_fullname}?{sas_token}"

    return blob_url
