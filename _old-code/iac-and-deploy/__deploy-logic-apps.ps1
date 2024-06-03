az login

az deployment group validate --resource-group "azure-sinistro-0704mvp" `
    --template-file C:\_Github\claim-automation-with-ai\logic-apps\logicapp0503mvp.connectors.json

az deployment group create --resource-group "azure-sinistro-0704mvp" `
    --template-file C:\_Github\claim-automation-with-ai\logic-apps\logicapp0503mvp.connectors.json

# az deployment group validate --resource-group "azure-logic-apps-deploy" `
#     --template-file deploy-template.json `
#     --parameters params.json

# az deployment group create --resource-group "azure-logic-apps-deploy" `
#     --template-file deploy-template.json `
#     --parameters params.json