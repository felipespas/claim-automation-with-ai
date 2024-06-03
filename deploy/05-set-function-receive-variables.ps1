# az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

Set-Location C:\_Github\claim-automation-with-ai\functions\func-receive

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\resourceGroupName.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionAppName = "fnreceiveapp" + $resourcesSuffix

#######################################################################################################################

# FUNCTION APP SETTINGS:

Write-Host "Resource Group Name: $resourceGroupName"

$eventHubNamespace = "eventhub$resourcesSuffix"

Write-Host "Event Hub Namespace: $eventHubNamespace"

$eventHubKey = Get-AzEventHubKey -ResourceGroupName $resourceGroupName -NamespaceName $eventHubNamespace -Name RootManageSharedAccessKey

$eventHubConnectionString = $eventHubKey.PrimaryConnectionString

Write-Host "Event Hub Connection String: $eventHubConnectionString"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "EVENT_HUB_CONNECTION_STR=$eventHubConnectionString"

$eventHubName = "incoming"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "EVENT_HUB_NAME=$eventHubName"