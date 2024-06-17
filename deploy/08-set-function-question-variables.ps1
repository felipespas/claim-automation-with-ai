# az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

Set-Location C:\_Github\claim-automation-with-ai\functions\func-question

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\resourceGroupName.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionAppName = "fnquestionapp" + $resourcesSuffix

#######################################################################################################################

# FUNCTION APP SETTINGS:

$dataLakeName = "datalake" + $resourcesSuffix

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "DATA_LAKE_NAME=$dataLakeName"

# get the storage account connection string from the resource
$DataLakeKey = (Get-AzStorageAccountKey -ResourceGroupName $resourceGroupName -Name $dataLakeName).Value[0]

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "DATA_LAKE_KEY=$DataLakeKey"

$storageJsonContainerName="jsons"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "CONTAINER_NAME_FOR_JSONS=$storageJsonContainerName"

#######################################################################################################################

# FIXED PARAMETERS

$azureOpenAIKey="9c49d2f8e3d84767bea9c23c2439c38e"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "AZURE_OPENAI_API_KEY=$azureOpenAIKey"

$azureOpenAIEndpoint="https://openai1704canadaeast.openai.azure.com/"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "AZURE_OPENAI_ENDPOINT=$azureOpenAIEndpoint"

$azureOpenAIVersion="2023-07-01-preview"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "AZURE_OPENAI_API_VERSION=$azureOpenAIVersion"

$azureOpenAIDeployment="gpt-4"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "AZURE_OPENAI_DEPLOYMENT=$azureOpenAIDeployment"