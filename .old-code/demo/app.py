import json
from openai import AzureOpenAI

client = AzureOpenAI(
    api_version="2023-07-01-preview",
    azure_endpoint="",
    api_key=""
)

# read the file input-cliente.txt and store it in a variable
with open('attachments\input-cliente.txt', 'r', encoding='utf-8') as file:
    claim = file.read()

# read the file database\apolice-seguro.json
with open('database\\apolice-seguro.json', 'r', encoding='utf-8') as file:
    policy = file.read()

# convert policy to json
policy = json.loads(policy)

coberturas_array = []

# iterate over coberturas inside policy document
for cobertura in policy['apólice']['coberturas']:
    tipo = cobertura['tipo']
    valor_coberto = cobertura['valor_coberto']
    
    # append to coberturas array
    coberturas_array.append(f"{tipo} - {valor_coberto}")

# convert coberturas array to string
coberturas_str = ', '.join(coberturas_array)

conversation = [
        {
            "role": "assistant",
            "content": "Você é um assistente responsável por verificar se a reclamação do cliente é cobertar na apolice de seguro fornecida. \
                Estas são as cobeerturas do seguro que o cliente tem: " + coberturas_str + ". \
                    E esta é a reclamação do cliente: " + claim + ". \
                        Responda as pergunta do usuário usando somente o contexto fornecido."            
        },
        {
            "role": "user",
            "content": "A reclamação do cliente se enquadra na cobertura da apólice dele? Responda com SIM ou NÃO."
        },
    ]

completion = client.chat.completions.create(
    model="chat",
    messages=conversation
)

# capture the property "choices" from the completion
choices = completion.choices[0]

response = choices.message.content

# print the response
print(response)

# print(completion.model_dump_json(indent=2))