# az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

Set-Location C:\_Github\ms-poc-sinistro-ai\func-sinistro

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\resourceGroupName.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionAppName = "functionwrapapp" + $resourcesSuffix

#######################################################################################################################

# FUNCTION APP SETTINGS:

$eventHubNamespace = "eventhub$resourcesSuffix"

$eventHubConnectionString = (Get-AzEventHubNamespace -ResourceGroupName $resourceGroupName -Name $eventHubNamespace).PrimaryConnectionString

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "EVENT_HUB_CONNECTION_STR=$eventHubConnectionString"

$eventHubName = "incoming"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "EVENT_HUB_NAME=$eventHubName"