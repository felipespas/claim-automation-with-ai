from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup

def clean_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    cleaned_text = soup.get_text(separator=' ') \
        .replace("\n", " ").replace("\r", " ").replace("\t", "") \
            .replace("\xa0", "").replace("‌&nbsp;", "").replace("\u200c", "") \
                .replace("  ", " ").strip()
    
    return cleaned_text

def extract_content_from_eml(eml_content):
    
    msg = BytesParser(policy=policy.default).parsebytes(eml_content)

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