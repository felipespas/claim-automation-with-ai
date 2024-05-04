# az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

Set-Location C:\_Github\ms-poc-sinistro-ai\func-sinistro

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\resourceGroupName.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionAppName = "functionapp" + $resourcesSuffix

#######################################################################################################################

# FUNCTION APP SETTINGS:

$dataLakeName = "datalake" + $resourcesSuffix

# set an azure function app setting
$dataLakeUrl = "https://" + $dataLakeName + ".dfs.core.windows.net/"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "DATA_LAKE_URL_ENDPOINT=$dataLakeUrl"

# get the storage account connection string from the resource
$storageAccountKey = (Get-AzStorageAccountKey -ResourceGroupName $resourceGroupName -Name $dataLakeName).Value[0]

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "STORAGE_ACCOUNT_KEY=$storageAccountKey"

$storageAccountConnectionString="DefaultEndpointsProtocol=https;AccountName="+$dataLakeName+";AccountKey="+$storageAccountKey+";EndpointSuffix=core.windows.net"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "STORAGE_ACCOUNT_CONNECTION_STRING=$storageAccountConnectionString"

$aiServicesName = "aiservices" + $resourcesSuffix

# get the key from the ai services endpoint
$aiServiceKey = (Invoke-AzResourceAction `
    -Action listKeys `
    -ResourceType 'Microsoft.CognitiveServices/accounts' `
    -ResourceGroupName $resourceGroupName `
    -ResourceName $aiServicesName `
    -Force).key1

# whow the key
Write-Host "AI Service Key: $aiServiceKey"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "AISERVICES_KEY=$aiServiceKey"

$aiServiceEndpoint = (Get-AzCognitiveServicesAccount -ResourceGroupName $resourceGroupName -Name $aiServicesName).Endpoint

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "AISERVICES_ENDPOINT=$aiServiceEndpoint"

$emailFolder = "emails"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "STORAGE_ACCOUNT_CONTAINER_EMAILS=$emailFolder"

$jsonFolder = "jsons"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "STORAGE_ACCOUNT_CONTAINER_JSONS=$jsonFolder"