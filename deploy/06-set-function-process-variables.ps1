# az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

Set-Location C:\_Github\claim-automation-with-ai\functions\func-process

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\resourceGroupName.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionAppName = "fnprocessapp" + $resourcesSuffix

#######################################################################################################################

# FUNCTION APP SETTINGS:

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

$dataLakeName = "datalake" + $resourcesSuffix

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "DATA_LAKE_NAME=$dataLakeName"

# get the storage account connection string from the resource
$dataLakeKey = (Get-AzStorageAccountKey -ResourceGroupName $resourceGroupName -Name $dataLakeName).Value[0]

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "DATA_LAKE_KEY=$dataLakeKey"

$emailContainer = "emails"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "CONTAINER_NAME_FOR_EMAILS=$emailContainer"

$jsonContainer = "jsons"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "CONTAINER_NAME_FOR_JSONS=$jsonContainer"

$eventHubIncoming

# EVENT HUB

$eventHubNamespace = "eventhub$resourcesSuffix"

Write-Host "Event Hub Namespace: $eventHubNamespace"

$eventHubKey = Get-AzEventHubKey -ResourceGroupName $resourceGroupName -NamespaceName $eventHubNamespace -Name RootManageSharedAccessKey

$eventHubConnectionString = $eventHubKey.PrimaryConnectionString

Write-Host "Event Hub Connection String: $eventHubConnectionString"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "EVENT_HUB_CONNECTION_STR=$eventHubConnectionString"

$eventHubName = "incoming"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "EVENT_HUB_NAME=$eventHubName"