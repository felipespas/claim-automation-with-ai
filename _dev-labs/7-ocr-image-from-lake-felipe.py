import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas

connection_string = "DefaultEndpointsProtocol=https;AccountName=datalake1705mvp;AccountKey=+JLA9gdxANoq+Y+xYMaQvTSiCjYT0v3cDBzwHrQAilkpc65/rnS0wdAZma9WvoKx7oQpPK2sOxE2+ASt4d+d7w==;EndpointSuffix=core.windows.net"
container_name = "data"
blob_name = "1/Redes de proteção.jpeg"

load_dotenv()

try:
    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    print("Set them before running this sample.")
    exit()

# Create a blob client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
blob_client = blob_service_client.get_blob_client(container_name, blob_name)

# Define the expiry time (1 hour from now in this example)
expiry_time = datetime.utcnow() + timedelta(hours=1)

# Generate SAS token
sas_token = generate_blob_sas(
    blob_service_client.account_name,
    container_name,
    blob_name,
    account_key=blob_service_client.credential.account_key,
    permission=BlobSasPermissions(read=True),
    expiry=expiry_time
)

blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

result = client.analyze_from_url(
    image_url=blob_url,
    # image_url="https://datalake1705mvp.blob.core.windows.net/data/1/Redes de proteção.jpeg",
    visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
    gender_neutral_caption=True,  # Optional (default is False)
)

print("Image analysis results:")

# Print caption results to the console
print(" Caption:")
if result.caption is not None:
    print(f"   '{result.caption.text}', Confidence {result.caption.confidence:.4f}")

# Print text (OCR) analysis results to the console
print(" Read:")
if result.read is not None:
    for line in result.read.blocks[0].lines:
        print({line.text})
