# First, log in to Azure with:
az login

# Set the subscription
az account set --subscription ""

# create the infrastructure for the azure function
# az storage account create --name storage1704mvp --location eastus `
#     --resource-group azure-mvp-sinistro --sku Standard_LRS

# # create the function app
# az functionapp create --resource-group azure-mvp-sinistro --os-type Linux `
#     --consumption-plan-location eastus --runtime python --runtime-version 3.11 `
#     --functions-version 4 --name functionapp0503mvp --storage-account storage1704mvp

# # # Then, navigate to the project directory (in case you're not there already)
# # cd mvp\funcs-sinistro

# # Then, publish the function with:
func azure functionapp publish functionapp0503mvp --python

func azure functionapp list-functions functionapp0503mvp