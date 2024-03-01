############################################################################
# AUTHENTICATE

# First, log in to Azure with:
az login

# Set the subscription
az account set --subscription "MCAPS-Hybrid-REQ-37753-2022-Fassis"

############################################################################
# IAC DEPLOY

cd .\mvp\pipelines\iac

rm .\.terraform.*
rm .\terraform*

# terraform commands
terraform init -upgrade

terraform init

terraform plan

terraform apply -auto-approve

############################################################################
# PERMISSIONS

# grant permission to the service principal as blob data contributor in the storage account
az role assignment create --assignee-object-id b05164da-c893-4a65-8046-edf9d90e792a `
    --assignee-principal-type ServicePrincipal `
    --role "Storage Blob Data Contributor" `
    --scope "/subscriptions/2edd29f5-689f-48c5-b93e-93723216ea91/resourceGroups/azure-mvp-sinistro-1705/providers/Microsoft.Storage/storageAccounts/datalake1705mvp"

############################################################################
# CODE DEPLOY 

# Navigate to the project directory (in case you're not there already)
cd ..\..\azure-function

# Then, publish the function with:
func azure functionapp publish functionapp1705mvp --python

func azure functionapp list-functions functionapp1705mvp
