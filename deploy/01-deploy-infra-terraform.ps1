az login

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path .\suffix.txt

# show the value
Write-Host "Resources Suffix: $resourcesSuffix"

terraform init

terraform plan -var="suffix=$resourcesSuffix"

terraform apply -auto-approve -var="suffix=$resourcesSuffix"

# terraform destroy -auto-approve -var="suffix=$resourcesSuffix"