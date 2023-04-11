import json
import pyodbc

# config file with access creds to the database
with open('Democode\\config.json') as f:
    d = json.load(f)

hostname = d['hostname']
user     = d['username']
psw      = d['psw']
database = 'hotel'

# Specifying the ODBC driver, server name, database, etc. directly
# create a connection object 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='
                      +hostname+';DATABASE='+database+';UID='
                      +user+';PWD='+psw+';TrustServerCertificate=yes')

print("Connection Attributes")
print(f"Autocommit = {cnxn.autocommit}")
print(f"Timeout seconds = {cnxn.timeout}\n")

# Create a cursor object from the connection
cursor = cnxn.cursor()

cursor.execute("SELECT  CONVERT(VARCHAR, GETDATE(), 13) AS DB_Time;")

row = cursor.fetchone() 
print(row)

cnxn.close()