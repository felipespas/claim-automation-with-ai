import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
azure_openai_api_version = os.environ["AZURE_OPENAI_API_VERSION"]
azure_openai_deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]

client = AzureOpenAI(
    api_version=azure_openai_api_version,
    azure_endpoint=azure_openai_endpoint,
)

def make_question(question: str, context: str):
    messages = [
            {
                "role": "system",
                "content": "Você é um assistente que responde às perguntas do usuário com base no contexto fornecido. \
                    Para responder, use sempre o mesmo idioma utilizado na pergunta.",
            },
            {
                "role": "user",
                "content": f"Aqui está todo o contexto que você conhece: {context}. \
                    Com base nisso, responda a pergunta do usuário: {question}"
            },
        ]

    completion = client.chat.completions.create(
        model=azure_openai_deployment,
        messages=messages,
    )

    response = completion.choices[0].message.content
    tokens = completion.usage.total_tokens

    return response, tokens