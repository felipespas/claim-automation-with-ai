az deployment group validate --resource-group "azure-logic-apps-deploy" `
    --template-file deploy-template.json `
    --parameters params.json

az deployment group create --resource-group "azure-logic-apps-deploy" `
    --template-file deploy-template.json `
    --parameters params.json