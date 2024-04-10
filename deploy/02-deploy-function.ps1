# az login

cd C:\_Github\ms-poc-sinistro-ai\func-sinistro

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\resourceGroupName.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionAppName = "functionapp" + $resourcesSuffix

# show the value for functionAppName variable
Write-Host "Function Name: $functionAppName"

# show the value
Write-Host "Resource Group Name: $resourceGroupName"

func azure functionapp publish $functionAppName --python

# func azure functionapp list-functions $functionAppName

$funcName = "prepare01"

$funcKey = (Invoke-AzResourceAction `
    -Action listKeys `
    -ResourceType 'Microsoft.Web/sites/functions/' `
    -ResourceGroupName $resourceGroupName `
    -ResourceName "$functionAppName/$funcName" `
    -Force).default

# show the value
Write-Host "Function Key: $funcKey"

$keyVaultName = "keyvault" + $resourcesSuffix + "2"

$secretName = $funcName + "-key"

# Power shell to create a secret in the key vault
$secretValue = ConvertTo-SecureString -String $funcKey -AsPlainText -Force

# Power shell to create a secret in the key vault
Set-AzKeyVaultSecret -VaultName $keyVaultName -Name $secretName -SecretValue $secretValue