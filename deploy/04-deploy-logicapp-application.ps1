# az login

cd C:\_Github\ms-poc-sinistro-ai\deploy

# read the value from suffix.txt file
$resourceSuffix = Get-Content -Path .\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path .\resourceGroupName.txt

$logicappsname = "logicapp$resourceSuffix"

$datalakename = "datalake$resourceSuffix"

# show the value for functionName variable
Write-Host "Suffix: $resourceSuffix"

# show the value
Write-Host "Resource Group Name: $resourceGroupName"

# show the value
Write-Host "Logic App Name: $logicappsname"

# show the value
Write-Host "Data Lake Name: $datalakename"

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
    --parameters logic_apps_name=$logicappsname workflows_parameters_storageaccount_name=$datalakename
    
az deployment group create --resource-group $resourceGroupName `
    --template-file C:\_Github\ms-poc-sinistro-ai\logic-apps\logicapp.definition.json `
    --parameters $paramsFilePath `
    --parameters logic_apps_name=$logicappsname workflows_parameters_storageaccount_name=$datalakename