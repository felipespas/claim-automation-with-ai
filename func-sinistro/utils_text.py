import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

container_name = os.environ["STORAGE_CONTAINER_FILES"]

def remove_html(text: str) -> str:
    cleaned_text = BeautifulSoup(text, features="html.parser").get_text()
    return cleaned_text

def validate_path(text: str) -> str:    
    # check if the first character is a slash and remove it
    if text[0] == "/":
        text = text[1:]

    # check if the first "folder" is the container
    container_name = text.split("/")[0]
    if container_name == os.environ["STORAGE_CONTAINER_FILES"]:
        text = text.replace(container_name + "/", "")

    return text