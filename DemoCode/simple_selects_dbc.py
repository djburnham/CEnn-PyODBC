import json
import pyodbc

def printCursorResInfo(cursor):
        print('\n**Result description from cursor**')
        for column in cursor.description:
                print('Name: ' + column[0])
                print('Python type: ' + str(column[1]))
                print('Nullable: ' + str(column[6]) + '\n')

# config file with access creds to the database
with open('DemoCode\\config.json') as f:
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

# Create a cursor object from the connection
cursor = cnxn.cursor()
# execute a statement with the cursor object 
cursor.execute("SELECT hotel_code, hotel_name FROM hotel;") 
# Print out the cursor metadata for the last call
printCursorResInfo(cursor)
# fetch the results one by one 
row = cursor.fetchone()
print( f"Python type returned from call to cursor.fetchone is : {type(row)}\n")
while row: 
    print(row[0], row[1])
    row = cursor.fetchone()
input("\nPress return to continue")
#
cursor.execute("SELECT title, first_name, last_name, birth_date, points FROM dbo.guest;")
# Print out the cursor metadata for the last call
printCursorResInfo(cursor)

allRows = cursor.fetchall()
print( f"Python type returned from call to cursor.fetchall is : {type(allRows)}")
print(f"This is a list of : {type(allRows[0])}\n" )

for row in allRows:
    print(row)

input("\nPress return to continue")

cursor.execute("SELECT transaction_id, account_num, ref, memo FROM dbo.account;")

# Print out the cursor metadata for the last call
printCursorResInfo(cursor)
# lets get 10 rows
manyRows = cursor.fetchmany(10)
print( f"Python type returned from call to cursor.fetchmany is : {type(manyRows)}")
print(f"This is a list of : {type(manyRows[0])}\n" )

for row in manyRows:
    print(row)
input("\nPress return to continue")

cursor.execute("SELECT ref FROM dbo.account WHERE transaction_id = 10050;")

# Print out the cursor metadata for the last call
printCursorResInfo(cursor)
# lets get a single value
SQLretVal = cursor.fetchval()
print(f"Returned value for ref column from SQL statement is {SQLretVal}")

input("\nPress return to continue")
cnxn.close()