# az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

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

terraform plan -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName" -var="location=$location" `
    -var="keyvaultSuffix=$keyvaultSuffix" -var="sqlPassword=$sqlPassword" -var="myIpAddress=$myIpAddress"

terraform apply -auto-approve -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName" -var="location=$location" `
    -var="keyvaultSuffix=$keyvaultSuffix" -var="sqlPassword=$sqlPassword" -var="myIpAddress=$myIpAddress"

# terraform destroy -auto-approve -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName" -var="location=$location" -var="keyvaultSuffix=$keyvaultSuffix"

# az group delete --name $resourceGroupName --yes --no-wait