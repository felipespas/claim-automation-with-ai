# az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

try{

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    # call the 01 script
    & '.\01-deploy-infra-terraform.ps1'

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    # call the 02 script
    & '.\02-deploy-function-receive.ps1'

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    # call the 03 script
    & '.\03-deploy-function-process.ps1'

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    # call the 04 script
    & '.\04-deploy-function-question.ps1'

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    # call the 05 script
    & '.\05-deploy-function-check.ps1'
    
    Set-Location C:\_Github\claim-automation-with-ai\deploy
    
    # call the 06 script
        & '.\06-set-function-receive-variables.ps1'

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    # call the 07 script
    & '.\07-set-function-process-variables.ps1'

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    # call the 08 script
    & '.\08-set-function-question-variables.ps1'

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    # call the 09 script
    & '.\09-set-function-check-variables.ps1'

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    # call the 10 script
    & '.\10-create-stored-procedure-sql.ps1'

    Set-Location C:\_Github\claim-automation-with-ai\deploy

    # call the 11 script
    & '.\11-deploy-logicapp-connectors.ps1'

    # print a message saying everything worked as planned
    Write-Host "All scripts executed successfully"
}
catch {
    Write-Host "Error in the script: $($_.InvocationInfo.ScriptName)"
    Write-Host "Error message: $($_.Exception.Message)"
    exit $_.Exception.HResult
}