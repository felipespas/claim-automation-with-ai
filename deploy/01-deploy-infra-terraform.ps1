az login

cd C:\_Github\ms-poc-sinistro-ai\terraform

# read the value from suffix.txt file
$resourceSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\resourceGroupName.txt

# show the value
Write-Host "Resources Suffix: $resourceSuffix"

# show the value
Write-Host "Resource Group Name: $resourceGroupName"

terraform init

terraform plan -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName"

terraform apply -auto-approve -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName"

# terraform destroy -auto-approve -var="suffix=$resourceSuffix" -var="resourceGroupName=$resourceGroupName"