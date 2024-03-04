from bs4 import BeautifulSoup

def remove_html(text: str) -> str:
    cleaned_text = BeautifulSoup(text, features="html.parser").get_text()

    return cleaned_text

