# Set the directory
Set-Location -Path "C:\_Github\claim-automation-with-ai\promptflow\deploy"

# Serve the flow at localhost:8080
pf flow serve --source ..\. --port 8080 --host localhost