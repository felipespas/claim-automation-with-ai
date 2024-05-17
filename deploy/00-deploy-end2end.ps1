az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

Set-Location C:\_Github\ms-poc-sinistro-ai\deploy

# call the 01 script
& '.\01-deploy-infra-terraform.ps1'

Set-Location C:\_Github\ms-poc-sinistro-ai\deploy

# call the 02 script
& '.\02-deploy-function-receive.ps1'

Set-Location C:\_Github\ms-poc-sinistro-ai\deploy

# call the 03 script
& '.\03-deploy-function-process.ps1'

Set-Location C:\_Github\ms-poc-sinistro-ai\deploy

# call the 04 script
& '.\04-set-function-process-variables.ps1'

Set-Location C:\_Github\ms-poc-sinistro-ai\deploy

# call the 05 script
& '.\05-set-function-receive-variables.ps1'

Set-Location C:\_Github\ms-poc-sinistro-ai\deploy

# call the 06 script
& '.\06-set-function-process-variables.ps1'

Set-Location C:\_Github\ms-poc-sinistro-ai\deploy

# call the 07 script
& '.\07-set-function-question-variables.ps1'

Set-Location C:\_Github\ms-poc-sinistro-ai\deploy

# call the 08 script
& '.\08-deploy-logicapp-connectors.ps1'