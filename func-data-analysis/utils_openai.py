from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_version="2023-07-01-preview",
    azure_endpoint="https://openai1704canadaeast.openai.azure.com/",
)

def make_question(question: str):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )
    print(completion.model_dump_json(indent=2))

    return completion.choices[0].message.content