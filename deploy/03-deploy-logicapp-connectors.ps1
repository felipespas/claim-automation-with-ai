# az login

# read the value from suffix.txt file
$resourceSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\resourceGroupName.txt

# read the value from suffix.txt file
$location = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\location.txt

# show the value for functionName variable
Write-Host "Suffix: $resourceSuffix"

# show the value
Write-Host "Resource Group Name: $resourceGroupName"

# show the value
Write-Host "Location: $location"

$json = "{\""suffix\"":{\""value\"":\""$resourceSuffix\""}, \""location\"":{\""value\"":\""$location\""}}"

write-Host "JSON: $json"

az deployment group validate --resource-group $resourceGroupName `
    --template-file C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp.connectors.json `
    --parameters $json

az deployment group create --resource-group $resourceGroupName `
    --template-file C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp.connectors.json `
    --parameters $json