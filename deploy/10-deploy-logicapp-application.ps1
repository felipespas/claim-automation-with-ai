# az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

Set-Location C:\_Github\ms-poc-sinistro-ai\deploy

# read the value from suffix.txt file
$resourceSuffix = Get-Content -Path .\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path .\resourceGroupName.txt

# show the value for functionName variable
Write-Host "Suffix: $resourceSuffix"

# show the value
Write-Host "Resource Group Name: $resourceGroupName"

# Define the path to the JSON file
$defaultParamsFilePath = "C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp.parameters.json"
$paramsFilePath = "C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp-modified.parameters.json"

# Read the content of the JSON file
$content = Get-Content $defaultParamsFilePath -Raw

# Replace the string
$oldString = "__resourceGroupName__"
$modifiedContent = $content -replace $oldString, $resourceGroupName

# Write the modified content back to the JSON file
$modifiedContent | Set-Content $paramsFilePath

az deployment group validate --resource-group $resourceGroupName `
    --template-file C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp.definition.json `
    --parameters $paramsFilePath `
    --parameters suffix=$resourceSuffix

az deployment group create --resource-group $resourceGroupName `
    --template-file C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp.definition.json `
    --parameters $paramsFilePath `
    --parameters suffix=$resourceSuffix