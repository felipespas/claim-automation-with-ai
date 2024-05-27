import pyodbc

# Define your connection string
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=tcp:mssqlserver150524.database.windows.net,1433;"
    "Database=sample;"
    "Uid=Felipe;"
    "Pwd=Enterprise001!;"
    "Encrypt=no;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

orderId = 71780

# Create a new connection
conn = pyodbc.connect(conn_str)

# Create a new cursor from the connection
cursor = conn.cursor()

# Execute the stored procedure
cursor.execute("{CALL p_ReturnOrderData (?)}", orderId)

# Get the column headers
column_headers = [column[0] for column in cursor.description]

print("Column Headers:", column_headers)

# If the stored procedure returns results, fetch them
results = cursor.fetchall()

for row in results:
    print(column_headers[0] + ":" + str(row[0]))
    print(column_headers[1] + ":" + str(row[1]))
    print(column_headers[2] + ":" + str(row[2]))
    print(column_headers[3] + ":" + str(row[3]))
    print(column_headers[4] + ":" + str(row[4]))
    print(column_headers[5] + ":" + str(row[5]))
    print(column_headers[6] + ":" + str(row[6]))
    print(column_headers[7] + ":" + str(row[7]))
    print(column_headers[8] + ":" + str(row[8]))
    print(column_headers[9] + ":" + str(row[9]))
    print(column_headers[10] + ":" + str(row[10]))
    print(column_headers[11] + ":" + str(row[11]))
    print(column_headers[12] + ":" + str(row[12]))
    print(column_headers[13] + ":" + str(row[13]))   
    print(column_headers[14] + ":" + str(row[14]))
    print("\n")

# Don't forget to close the connection when you're done
conn.close()