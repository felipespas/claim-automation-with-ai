try{

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    $tenant_id = "16b3c013-d300-468d-ac64-7eda0820b6d3"
    $subscription_id = "2edd29f5-689f-48c5-b93e-93723216ea91"

    .\connect-azure.ps1 $tenant_id $subscription_id

    Set-Location C:\_Github\claim-automation-with-ai\terraform

    # read the value from txt file
    $resourceSuffix = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\suffix.txt

    # show the value
    Write-Host "Resources Suffix: $resourceSuffix"

    # read the value from txt file
    $resourceGroupName = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\resourceGroupName.txt

    # show the value
    Write-Host "Resource Group Name: $resourceGroupName"

    # read the value from txt file
    $location = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\location.txt

    # show the value
    Write-Host "Location: $location"

    # read the value from txt file
    $keyvaultSuffix = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\keyvaultSuffix.txt

    # show the value
    Write-Host "Key Vault Suffix: $keyvaultSuffix"

    # read the sql server password from txt file
    $sqlPassword = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\sqlPassword.txt

    # show the value
    Write-Host "SQL Password: $sqlPassword"

    # obtain my current ip address
    $myIpAddress = (Invoke-RestMethod http://ipinfo.io/json).ip

    # show the value
    Write-Host "My IP Address: $myIpAddress"

    terraform init

    # terraform plan -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName" `
    #     -var="location=$location" -var="keyvaultSuffix=$keyvaultSuffix" -var="sqlPassword=$sqlPassword" `
    #     -var="myIpAddress=$myIpAddress" -var="subscription_id=$subscription_id"

    # $env:TF_LOG = "DEBUG"
    # $env:TF_LOG_PATH = "terraform.log"        

    terraform apply -auto-approve -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName" `
        -var="location=$location" -var="keyvaultSuffix=$keyvaultSuffix" -var="sqlPassword=$sqlPassword" `
        -var="myIpAddress=$myIpAddress" -var="subscription_id=$subscription_id"

    # $env:TF_LOG = ""
    # $env:TF_LOG_PATH = ""

    # terraform destroy -auto-approve -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName" `
    #    -var="location=$location" -var="keyvaultSuffix=$keyvaultSuffix" -var="sqlPassword=$sqlPassword" `
    #    -var="myIpAddress=$myIpAddress" -var="subscription_id=$subscription_id"

    # az group delete --name $resourceGroupName --yes --no-wait

    Set-Location C:\_Github\claim-automation-with-ai\deploy
}
catch{
    # print the error
    Write-Host "Error: $_"
    
    # return error status
    exit 1
}
