# Import the SQL Server module
Import-Module SqlServer

# read the value from txt file
$resourceSuffix = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\suffix.txt

# show the value
Write-Host "Resources Suffix: $resourceSuffix"

# Define the connection properties
$serverName = "mssqlserver" + $resourceSuffix + ".database.windows.net"

# show the value
Write-Host "Server: $serverName"

$databaseName = "sample"
$userId = "Felipe"

# read the sql server password from txt file
$sqlPassword = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\sqlPassword.txt

# show the value
Write-Host "SQL Password: $sqlPassword"

# Create a credential object
$securePassword = ConvertTo-SecureString $sqlPassword -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($userId, $securePassword)

# Define the path to the .sql file
$sqlFilePath = "C:\_Github\claim-automation-with-ai\promptflow\sql-codes\return-order-products-details.sql"

# Read the content of the .sql file
$sqlCommand = Get-Content -Path $sqlFilePath

# Convert the content to a single string
$sqlCommand = $sqlCommand -join "`n"

# Connect to the SQL Server and execute the SQL command
Invoke-Sqlcmd -ServerInstance $serverName -Database $databaseName -Credential $credential -Query $sqlCommand

# Call the stored procedure to validate it
$result = Invoke-Sqlcmd -ServerInstance $serverName -Database $databaseName -Credential $credential -Query "EXEC p_ReturnOrderDetails_JSON 71780"

# Get the result property from the result object
$result = $result.result

# Show the result
Write-Host $result