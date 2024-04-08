az login

# read the value from suffix.txt file
$resourcesSuffix = Get-Content -Path .\suffix.txt

# concatenate the value from variable $resourceSuffix with the string "mvp"
$functionName = "functionapp" + $resourcesSuffix

# show the value for functionName variable
Write-Host "Function Name: $functionName"

cd ..\func-sinistro

func azure functionapp publish $functionName --python

func azure functionapp list-functions $functionName