import os
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

load_dotenv()

def capture_text_from_image(blob_url: str): 

    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]

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