import requests
import json

# Create a dictionary with the data you want to send
data = {
    "directory": "638459383340000000",
    "question": "Quantos aparelhos foram comprados?"
}

# Define the URL of the Azure Function
url = 'http://localhost:7071/api/validate01'

# print the data as a formatted json
data = json.dumps(data, indent=4)

print(data)

# # Make a POST request to the Azure Function
response = requests.post(url, json=data)

# # # Print the response
print(response.text)