############################################################################
# AUTHENTICATE

# First, log in to Azure with:
az login

# Set the subscription
az account set --subscription ""

############################################################################
# IAC DEPLOY

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
    --scope ""

############################################################################
# CODE DEPLOY 

# Navigate to the project directory (in case you're not there already)
cd func-sinistro

# Then, publish the function with:
func azure functionapp publish functionapp1705mvp --python

func azure functionapp list-functions functionapp1705mvp
