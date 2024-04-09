# az login

cd C:\_Github\ms-poc-sinistro-ai\func-sinistro

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path C:\_Github\ms-poc-sinistro-ai\deploy\suffix.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionName = "functionapp" + $resourcesSuffix

# show the value for functionName variable
Write-Host "Function Name: $functionName"

func azure functionapp publish $functionName --python

func azure functionapp list-functions $functionName