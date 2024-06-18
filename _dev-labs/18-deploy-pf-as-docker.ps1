# azure login via powershell
az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

$ResourceGroup = "azure-promptflow-app01"

$appName = "pf02-app-170490"

# set the directory using powershell
Set-Location -Path "C:\_Github\claim-automation-with-ai\promptflow\deploy"

pf flow build --source . --output dist --format docker

# Create a resource group
az group create --name $ResourceGroup --location eastus

# Create a container registry
az acr create --resource-group $ResourceGroup --name "containerregistry1704" --sku Basic

# Log in to the container registry
# az acr login --name "containerregistry1704" --expose-token

Set-Location -Path "C:\_Github\claim-automation-with-ai\promptflow\dist"

# Build the Docker image and push it to the container registry
az acr build --registry "containerregistry1704" --image promptflowapp:v1 .

Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser

Set-Location -Path "C:\_Github\claim-automation-with-ai\promptflow\deploy"

# run the deploy script using powershell
.\deploy.ps1 -Path .\..\dist -i "promptflowapp:v1" -n $appName -r "containerregistry1704" -g $ResourceGroup

# set a variable environment for the web app
az webapp config appsettings set -g $ResourceGroup --name $appName --settings DATA_LAKE_NAME="datalake030624"

az webapp config appsettings set -g $ResourceGroup --name $appName --settings DATA_LAKE_KEY="ay/HkzhqC7b3XXLAU74UM7PcQlf5WqdjJ1jVTIOHNkR+84GDwJqdZR3hrbY12MM+mMtcG5d6e+SO+ASt+5WLaA=="

az webapp config appsettings set -g $ResourceGroup --name $appName --settings CONTAINER_NAME_FOR_JSONS="jsons"

az webapp config appsettings set -g $ResourceGroup --name $appName --settings SQL_CONN_STR="Driver={ODBC Driver 17 for SQL Server};Server=tcp:mssqlserver030624.database.windows.net,1433;Database=sample;Uid=Felipe;Pwd=Enterprise001!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;"

# restart web app
az webapp restart -g $ResourceGroup --name $appName