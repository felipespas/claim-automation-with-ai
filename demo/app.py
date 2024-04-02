import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
key = os.environ["AZURE_OPENAI_KEY"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
api_version = os.environ["AZURE_OPENAI_API_VERSION"]

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=key
)

# read the file input-cliente.txt and store it in a variable
with open('attachments\\input-cliente.txt', 'r', encoding='utf-8') as file:
    claim = file.read()

# read the file database\apolice-seguro.json
# with open('database\\apolice-seguro.json', 'r', encoding='utf-8') as file:
#     policy = file.read()

with open('database\\coberturas.txt', 'r', encoding='utf-8') as file:
    policy = file.read()

# convert policy to json
# policy = json.loads(policy)

# coberturas_array = []

# iterate over coberturas inside policy document
# for cobertura in policy['apólice']['coberturas']:
#     tipo = cobertura['tipo']
#     valor_coberto = cobertura['valor_coberto']
    
#     # append to coberturas array
#     coberturas_array.append(f"{tipo} - {valor_coberto}")

# convert coberturas array to string
# coberturas_str = ', '.join(coberturas_array)

conversation = [
        {
            "role": "assistant",
            "content": "Você é um assistente responsável por verificar se a reclamação do cliente é coberta na apolice de seguro fornecida. \
                Estas são as coberturas do seguro que o cliente tem: " + policy + ". \
                    E esta é a reclamação do cliente: " + claim + ". \
                        Responda as perguntas do usuário usando somente o contexto fornecido e informe qual cobetura melhor se aplique."            
        },
        {
            "role": "user",
            "content": "A reclamação do cliente se enquadra na cobertura da apólice dele? Responda com SIM ou NÃO. E qual cobetura melhor se aplica?"
        }
    ]

completion = client.chat.completions.create(
    model=deployment,
    messages=conversation
)

# capture the property "choices" from the completion
choices = completion.choices[0]

response = choices.message.content

# print the response
print(response)

# print(completion.model_dump_json(indent=2))
