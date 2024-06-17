# az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

Set-Location C:\_Github\claim-automation-with-ai\functions\func-check

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\resourceGroupName.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionAppName = "fncheckapp" + $resourcesSuffix

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

$azureOpenAIKey="9109fbe161b74eb8be93799a0954a230"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "AZURE_OPENAI_API_KEY=$azureOpenAIKey"

$azureOpenAIEndpoint="https://openai1704eastus.openai.azure.com/"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "AZURE_OPENAI_ENDPOINT=$azureOpenAIEndpoint"

$azureOpenAIVersion="2024-02-01"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "AZURE_OPENAI_API_VERSION=$azureOpenAIVersion"

$azureOpenAIDeployment="gpt-4o-2024-05-13-global"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "AZURE_OPENAI_DEPLOYMENT=$azureOpenAIDeployment"

#######################################################################################################################

# SQL SERVER

$sqlServerName = "mssqlserver" + $resourcesSuffix

# read the sql server password from txt file
$sqlPassword = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\sqlPassword.txt

# obtain the connection string for a specific database 
$SQL_CONN_STR="Driver={ODBC Driver 17 for SQL Server};Server=tcp:$sqlServerName.database.windows.net,1433;Database=sample;Uid=Felipe;Pwd=$sqlPassword;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;"

az functionapp config appsettings set --name $functionAppName --resource-group $resourceGroupName --settings "SQL_CONN_STR=$SQL_CONN_STR"

