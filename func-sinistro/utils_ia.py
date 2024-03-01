import os
import re
import json
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

endpoint = os.environ["VISION_ENDPOINT"]
key = os.environ["VISION_KEY"]

def capture_text_from_image(image_url: str):     

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    result = client.analyze_from_url(
        image_url=image_url,
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

def capture_text_from_pdf(blob_url: str):

    client = DocumentAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    poller = client.begin_analyze_document_from_url("prebuilt-document", blob_url)
    result = poller.result()
    
    result_text = '['
    try:
        for pair in result.key_value_pairs:

            if pair.key and pair.key.content:
                key_content = pair.key.content.replace("\n", "\\n").replace("/", "\/")
                    
            if pair.value and pair.value.content:
                value_content = pair.value.content.replace("\n", "\\n").replace("/", "\/")
            else:
                value_content = ""

            result_text += "{\"" + key_content + "\": \"" + value_content + "\"}"

            # check if it's the last pair
            if not pair == result.key_value_pairs[-1]:
                result_text += ","           

        # remove the last comma and space
        result_text += "]"
        
        # convert string to json
        result_json = json.loads(result_text)
        
    except Exception as e:
        print(str(e))

    return result_json