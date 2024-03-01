Invoke-RestMethod -Method Post `
    -Uri https://function-name.azurewebsites.net/api/endpoint-name?code=access-code `
    -Body '{"name": "Felipe"}'