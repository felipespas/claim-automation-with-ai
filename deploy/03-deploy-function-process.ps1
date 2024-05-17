# az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

Set-Location C:\_Github\ms-poc-sinistro-ai\functions\func-process

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\resourceGroupName.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionAppName = "fnprocessapp" + $resourcesSuffix

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

##############################################################################################

$funcName = "process01"

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

