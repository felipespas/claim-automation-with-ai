############################################################################
# AUTHENTICATE

# First, log in to Azure with:
az login

# Set the subscription
az account set --subscription "MCAPS-Hybrid-REQ-37753-2022-Fassis"

############################################################################
# IAC DEPLOY

cd .\pipelines\iac\



############################################################################
# PERMISSIONS

# grant permission to me (felipe de assis) in the storage account
az role assignment create --assignee-object-id 200d5c65-b7ae-42ec-9c5a-978b410ee830 `
    --assignee-principal-type ServicePrincipal `
    --role "Storage Blob Data Contributor" `
    --scope "/subscriptions/2edd29f5-689f-48c5-b93e-93723216ea91/resourceGroups/azure-mvp-sinistro/providers/Microsoft.Storage/storageAccounts/datalake0503mvp/blobServices/default"  

############################################################################
# CODE DEPLOY 

# Navigate to the project directory (in case you're not there already)
cd ..\..\func-sinistro

# Then, publish the function with:
func azure functionapp publish functionapp0503mvp --python

func azure functionapp list-functions functionapp0503mvp
