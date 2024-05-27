import pyodbc
import json

# Define your connection string
# conn_str = (
#     "Driver={ODBC Driver 17 for SQL Server};"
#     "Server=tcp:mssqlserver150524.database.windows.net,1433;"
#     "Database=sample;"
#     "Uid=Felipe;"
#     "Pwd=Enterprise001!;"
#     "Encrypt=no;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
# )

conn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=tcp:mssqlserver150524.database.windows.net,1433;Database=sample;Uid=Felipe;Pwd=Enterprise001!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;")

orderId = 71780

# Create a new connection
conn = pyodbc.connect(conn_str)

# Create a new cursor from the connection
cursor = conn.cursor()

# Execute the stored procedure
cursor.execute("{CALL p_ReturnOrderData_JSON (?)}", orderId)

# Fetch the JSON document as a string
results = cursor.fetchone()[0]

# save results into a file
with open('output.txt', 'w') as f:
    f.write(results)

# Parse the JSON string into a Python object
data = json.loads(results)

# save results into a file
# with open('output.json', 'w') as f:
#     f.write(str(data[0]))

# print json data in a formatted way, using indent = 4
print(json.dumps(data, indent=4))

# Don't forget to close the connection when you're done
conn.close()

