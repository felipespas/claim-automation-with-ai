# az login

Set-Location C:\_Github\ms-poc-sinistro-ai\terraform

# read the value from suffix.txt file
$resourceSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\resourceGroupName.txt

# read the value from suffix.txt file
$location = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\location.txt

# read the value from suffix.txt file
$keyvaultSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\keyvaultSuffix.txt

# show the value
Write-Host "Resources Suffix: $resourceSuffix"

# show the value
Write-Host "Resource Group Name: $resourceGroupName"

# show the value
Write-Host "Location: $location"

# show the value
Write-Host "Key Vault Suffix: $keyvaultSuffix"

terraform init

terraform plan -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName" -var="location=$location" -var="keyvaultSuffix=$keyvaultSuffix"

terraform apply -auto-approve -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName" -var="location=$location" -var="keyvaultSuffix=$keyvaultSuffix"

# terraform destroy -auto-approve -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName" -var="location=$location" -var="keyvaultSuffix=$keyvaultSuffix"