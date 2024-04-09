# az login

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\suffix.txt

$location = "eastus"

# show the value for functionName variable
Write-Host "Suffix: $resourcesSuffix"

$resourceGroupName = "azure-sinistro-$resourcesSuffix"

# show the value for functionName variable
Write-Host "Resource Group Name: $resourceGroupName"

$json = "{\""suffix\"":{\""value\"":\""$resourcesSuffix\""}, \""location\"":{\""value\"":\""$location\""}}"

write-Host "JSON: $json"

az deployment group validate --resource-group $resourceGroupName `
    --template-file C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp.connectors.json `
    --parameters $json

az deployment group create --resource-group $resourceGroupName `
    --template-file C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp.connectors.json `
    --parameters $json