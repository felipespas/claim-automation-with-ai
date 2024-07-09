try{
    # login to azure using powershell
    # Connect-AzAccount -Tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

    # set the subscription id
    Set-AzContext -Subscription "MCAPS-Hybrid-REQ-37753-2022-Fassis"

    Set-Location C:\_Github\claim-automation-with-ai\functions\func-question

    # read the value from suffix.txt file
    $resourcesSuffix = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\suffix.txt

    # read the value from suffix.txt file
    $resourceGroupName = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\resourceGroupName.txt

    # concatenate the value from variable $resourceSuffix with the string "mvp"
    $functionAppName = "fnquestionapp" + $resourcesSuffix

    # read the value from suffix.txt file
    $keyvaultSuffix = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\keyvaultSuffix.txt

    # show the value for functionAppName variable
    Write-Host "Function Name: $functionAppName"

    # show the value
    Write-Host "Resource Group Name: $resourceGroupName"

    # show the value
    Write-Host "Key Vault Suffix: $keyvaultSuffix"

    func azure functionapp publish $functionAppName --python

    # func azure functionapp list-functions $functionAppName

    ##############################################################################################

    $funcName = "question01"

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

    Set-Location C:\_Github\claim-automation-with-ai\deploy
}
catch{
    # print the error
    Write-Host "Error: $_"
    
    # return error status
    exit 1
}