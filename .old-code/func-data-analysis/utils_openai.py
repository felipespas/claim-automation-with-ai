import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
azure_openai_api_version = os.environ["AZURE_OPENAI_API_VERSION"]

client = AzureOpenAI(
    api_version=azure_openai_api_version,
    azure_endpoint=azure_openai_endpoint,
)

def make_question(question: str, content: str):
    messages = [
            {
                "role": "system",
                "content": "Você é um assistente que responde às perguntas do usuário com base no contexto fornecido. \
                    Para responder, use sempre o mesmo idioma utilizado na pergunta.",
            },
            {
                "role": "user",
                "content": f"Aqui está todo o contexto que você conhece: {content}. \
                    Com base nisso, responda a pergunta do usuário: {question}"
            },
        ]

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
    )

    return completion.choices[0].message.content