az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

# exec the step 01
C:\_Github\ms-poc-sinistro-ai\deploy\01-deploy-infra-terraform.ps1

# exec the step 02
C:\_Github\ms-poc-sinistro-ai\deploy\02-deploy-function.ps1

# exec the step 03
C:\_Github\ms-poc-sinistro-ai\deploy\03-set-function-app-variables.ps1

# exec the step 04
C:\_Github\ms-poc-sinistro-ai\deploy\04-deploy-logicapp-connectors.ps1

# exec the step 05
C:\_Github\ms-poc-sinistro-ai\deploy\05-deploy-logicapp-application.ps1