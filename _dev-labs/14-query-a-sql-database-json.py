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

productId = 680

# Create a new connection
conn = pyodbc.connect(conn_str)

# Create a new cursor from the connection
cursor = conn.cursor()

# Execute the stored procedure
cursor.execute("{CALL p_ReturnProductData (?)}", productId)

# Fetch the JSON document as a string
json_string = cursor.fetchone()[0]

# Parse the JSON string into a Python object
data = json.loads(json_string)

print(data)

# Don't forget to close the connection when you're done
conn.close()