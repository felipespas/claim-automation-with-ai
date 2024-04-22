# az login

Set-Location C:\_Github\ms-poc-sinistro-ai\deploy

# read the value from suffix.txt file
$resourceSuffix = Get-Content -Path .\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path .\resourceGroupName.txt

# read the value from suffix.txt file
$location = Get-Content -Path .\location.txt

# read the value from suffix.txt file
$keyvaultSuffix = Get-Content -Path .\keyvaultSuffix.txt

# show the value for functionName variable
Write-Host "Suffix: $resourceSuffix"

# show the value
Write-Host "Resource Group Name: $resourceGroupName"

# show the value
Write-Host "Location: $location"

# show the value
Write-Host "Key Vault Suffix: $keyvaultSuffix"

# $json = "{\""suffix\"":{\""value\"":\""$resourceSuffix\""}, \""location\"":{\""value\"":\""$location\""}}"

$json = "{\""suffix\"":{\""value\"":\""$resourceSuffix\""}, \""keyvaultSuffix\"":{\""value\"":\""$keyvaultSuffix\""}}"

write-Host "JSON: $json"

az deployment group validate --resource-group $resourceGroupName `
    --template-file C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp.connectors.json `
    --parameters $json

az deployment group create --resource-group $resourceGroupName `
    --template-file C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp.connectors.json `
    --parameters $json