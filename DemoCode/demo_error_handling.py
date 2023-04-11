# Script to illustrate error handling
import pyodbc
import json

def printCursorResInfo(cursor):
        print('\n**Result description from cursor**')
        for column in cursor.description:
                print('Name: ' + column[0])
                print('Python type: ' + str(column[1]))
                print('Nullable: ' + str(column[6]) + '\n')
        
# config file with access creds to the database
with open('DemoCode//config_local.json') as f:
    d = json.load(f)

hostname = d['hostname']
user     = d['username']
psw      = d['psw']
database = 'bikeshop'

connectString = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+\
hostname+';DATABASE='+database+';UID='+\
user+';PWD='+psw+';TrustServerCertificate=yes'

input(" shutdown the local SQL database!") 
try:
    cnxn = pyodbc.connect(connectString)
except pyodbc.OperationalError as pyodbcerror:
    print(f"Error {str(pyodbcerror)}")
    input("\nStart the database now  Press return to continue")

# startup the local database and get the connection 

cnxn = pyodbc.connect(connectString)
# Create a cursor object from the connection
cursor = cnxn.cursor()
cursor.setinputsizes([(pyodbc.SQL_WVARCHAR, 50, 0)])
#autocommit False by default
print(f"Autocommit is {str(cnxn.autocommit)}\n")
input("\nEstablished a connection  Press return to run disconnect demo\n")
print("Database Disconnect Demo")
sql = "WAITFOR DELAY '00:01:30';"
try:
    cursor.execute(sql)
    rows = cursor.fetchall()
except pyodbc.Error as pyodbcerror:
    print(f"Error {str(pyodbcerror)}")
    cnxn.close()

input("\nStart SQL Server again and press enter to continue to PK violation error\n")

print("Data Integrity failure - Primary key violation")
# need to re-establish the connection 
cnxn = pyodbc.connect(connectString)
# Create a cursor object from the connection
cursor = cnxn.cursor()
cursor.setinputsizes([(pyodbc.SQL_WVARCHAR, 50, 0)])

sql = """UPDATE [sales].[customers_copy]
        SET customer_id = 1
        WHERE customer_id IN (10, 11, 12);"""
try:
    cursor.execute(sql)
    rows = cursor.fetchall()
except pyodbc.IntegrityError as pyodbcerror:
    print(f"Error {str(pyodbcerror)}")

input("\nPress enter to continue, to the Data Error Demo")

sql = "SELECT CAST(999999999999999 AS int);"
try:
    cursor.execute(sql)
    rows = cursor.fetchall()
except pyodbc.DataError as pyodbcerror:
    print(f"Error {str(pyodbcerror)}")

input("\nPress return to End")
    
    
          