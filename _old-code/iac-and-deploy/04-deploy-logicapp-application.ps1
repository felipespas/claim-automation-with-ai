# az login

# read the value from suffix.txt file
# $resourceSuffix = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\suffix.txt

# read the value from suffix.txt file
$resourceGroupName = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\resourceGroupName.txt

# read the value from suffix.txt file
# $location = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\location.txt

# $logicappsname = "logicapp$resourceSuffix"

# show the value for functionName variable
Write-Host "Suffix: $resourceSuffix"

# show the value
Write-Host "Resource Group Name: $resourceGroupName"

# show the value
# Write-Host "Location: $location"

# show the value
# Write-Host "Logic App Name: $logicappsname"

# $json = "{\""suffix\"":{\""value\"":\""$resourceSuffix\""}, \""location\"":{\""value\"":\""$location\""}}"

# $json = "{\""logic_apps_name\"":{\""value\"":\""$logicappsname\""}}"

# write-Host "JSON: $json"

az deployment group validate --resource-group $resourceGroupName `
    --template-file C:\_Github\claim-automation-with-ai\logic-apps\logicapp.definition.json `
    --parameters C:\_Github\claim-automation-with-ai\logic-apps\logicapp.parameters.json
    
az deployment group create --resource-group $resourceGroupName `
    --template-file C:\_Github\claim-automation-with-ai\logic-apps\logicapp.definition.json `
    --parameters C:\_Github\claim-automation-with-ai\logic-apps\logicapp.parameters.json