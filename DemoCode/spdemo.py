# Script to execute a stored procedure that returns
# multiple result sets 

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
database = 'Northwind'

connectString = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+\
hostname+';DATABASE='+database+';UID='+\
user+';PWD='+psw+';TrustServerCertificate=yes'

# We can use a python context manager with pyodbc.connect()
with  pyodbc.connect(connectString) as cnxn:
    # Create a cursor object from the connection
    cursor = cnxn.cursor()
    cursor.setinputsizes([(pyodbc.SQL_WVARCHAR, 50, 0)])
    # execute the stored proc with the cursor object 
    custID = 'AROUT'
    tSql = '{CALL [dbo].[FullCustOrderHist] (?) }'
    cursor.execute(tSql, custID)

    input("\nPress return to continue")
    # Print out the cursor metadata for the last call
    allRows = cursor.fetchall()
    while allRows:       
        printCursorResInfo(cursor)
        # print out the row
        for row in allRows:
            print(row)
     
        if cursor.nextset():
            allRows = cursor.fetchall()
        else:
            allRows = None
        
    input("\nPress return to continue")
