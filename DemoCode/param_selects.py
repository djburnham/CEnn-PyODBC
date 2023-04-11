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
hname = 'Southwark Hotel'
cursor.execute("SELECT hotel_code FROM hotel where hotel_name = ? ;", hname )
hname = 'London Heathrow Lodge' 
cursor.execute("SELECT hotel_code FROM hotel where hotel_name = ? ;", hname )
input("\nPress return to continue")

# Set the default for converting strings to SQL varchar(50)
cursor.setinputsizes([(pyodbc.SQL_WVARCHAR, 50, 0)])
guestName = 'Ian'
cursor.execute("SELECT guest_id FROM guest where first_name = ? ;", guestName )
guestName = 'Cassandra'
cursor.execute("SELECT guest_id FROM guest where first_name = ? ;", guestName )
input("\nPress return to continue")

# Print out the cursor metadata for the last call
printCursorResInfo(cursor)
# fetch the results one by one 
#
allRows = cursor.fetchall()
print( f"Python type returned from call to cursor.fetchall is : {type(allRows)}")
print(f"This is a list of : {type(allRows[0])}\n" )

for row in allRows:
    print(row)

input("\nPress return to continue")

cnxn.close()