import os
# import eml_parser
# import json
from email import policy
from email.parser import BytesParser
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from azure.storage.filedatalake import DataLakeServiceClient

load_dotenv()

connection_string = os.environ["STORAGE_CONNECTION_STRING"]
files_container_name = os.environ["STORAGE_CONTAINER_FILES"]
jsons_container_name = os.environ["STORAGE_CONTAINER_JSONS"]
storage_account_key = os.environ["STORAGE_ACCOUNT_KEY"]
storage_account_url = os.environ["DATA_LAKE_URL_ENDPOINT"]

def validate_path(text: str) -> str:    
    # check if the first character is a slash and remove it
    if text[0] == "/":
        text = text[1:]

    # check if the first "folder" is the container
    container_name = text.split("/")[0]
    if container_name == files_container_name:
        text = text.replace(container_name + "/", "")

    return text

def clean_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    cleaned_text = soup.get_text(separator=' ') \
        .replace("\n", " ").replace("\r", " ").replace("\t", "") \
            .replace("\xa0", "").replace("‌&nbsp;", "").replace("\u200c", "") \
                .replace("  ", " ").strip()
    
    return cleaned_text

def extract_content_from_eml(file_path):
    
    # Create a DataLakeServiceClient object
    service_client = DataLakeServiceClient(account_url=storage_account_url, credential=storage_account_key)

    # Get the file system client
    file_system_client = service_client.get_file_system_client(files_container_name)

    # Get the data lake file client
    file_client = file_system_client.get_file_client(file_path)

    # Download the content of the file into a variable
    download_stream = file_client.download_file()
    downloaded_content = download_stream.readall()

    # ep = eml_parser.EmlParser()
    # parsed_eml = ep.decode_email_bytes(downloaded_content)
    
    msg = BytesParser(policy=policy.default).parsebytes(downloaded_content)

    # Now you can access the email parts
    subject = msg['subject']
    from_address = msg['from']
    to_address = msg['to']
    body = clean_html(msg.get_body(preferencelist=('plain', 'html')).get_content())

    email_dict = {
        'subject': subject,
        'from': from_address,
        'to': to_address,
        'body': body
    }

    result_json = {
        "content": email_dict
    }

    return result_json