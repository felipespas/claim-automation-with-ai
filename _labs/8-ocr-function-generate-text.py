import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas

def capture_text_from_image(blob_fullname: str): 

    load_dotenv()

    try:
        endpoint = os.environ["VISION_ENDPOINT"]
        key = os.environ["VISION_KEY"]
        connection_string = os.environ["STORAGE_CONNECTION_STRING"]
        container_name = os.environ["STORAGE_CONTAINER_NAME"]
    except KeyError:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
        print("Set them before running this sample.")
        exit()

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

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    result = client.analyze_from_url(
        image_url=blob_url,
        visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
        gender_neutral_caption=True
    )

    # Capture caption and confidence from the image
    caption = ""
    confidence = ""
    if result.caption is not None:
        caption = result.caption.text
        confidence = result.caption.confidence

    # Capture all texts from the image
    fulltext = ''
    if result.read is not None:
        for line in result.read.blocks[0].lines:
            fulltext += str(line.text) + " "

    result_json = {
        "caption": caption,
        "confidence": confidence,
        "fulltext": fulltext
    }

    return result_json

if __name__ == "__main__":
    
    blob_fullname = "1/Redes de proteção.jpeg"
    result_json = str(capture_text_from_image(blob_fullname))
    
    print("")
    print(f"saída da function: {result_json}")
    
