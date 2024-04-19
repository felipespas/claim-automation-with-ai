# az login

Set-Location C:\_Github\ms-poc-sinistro-ai\func-sinistro

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\resourceGroupName.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionAppName = "functionapp" + $resourcesSuffix

# read the value from suffix.txt file
$keyvaultSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\keyvaultSuffix.txt

# show the value for functionAppName variable
Write-Host "Function Name: $functionAppName"

# show the value
Write-Host "Resource Group Name: $resourceGroupName"

# show the value
Write-Host "Key Vault Suffix: $keyvaultSuffix"

func azure functionapp publish $functionAppName --python

# func azure functionapp list-functions $functionAppName

$funcName = "prepare01"

# obtain the endpoint key for the function app
$funcKey = (Invoke-AzResourceAction `
    -Action listKeys `
    -ResourceType 'Microsoft.Web/sites/functions/' `
    -ResourceGroupName $resourceGroupName `
    -ResourceName "$functionAppName/$funcName" `
    -Force).default

# show the value
Write-Host "Function Key: $funcKey"

$keyVaultName = "keyvault" + $resourcesSuffix + $keyvaultSuffix

# show the value of $keyVaultName parameter
Write-Host "Key Vault Name: $keyVaultName"

$secretName = $funcName + "-key"

# Power shell to create a secret in the key vault
$secretValue = ConvertTo-SecureString -String $funcKey -AsPlainText -Force

# Power shell to create a secret in the key vault
Set-AzKeyVaultSecret -VaultName $keyVaultName -Name $secretName -SecretValue $secretValue

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