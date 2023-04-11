# Script to illustrate selecting a spatial type with no conversion  

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
    
    # Select on a Geography type in Earthquakeinformation
    Sql = '''SELECT EarthquakeID, Earthquakeinformation
            FROM [djbpyodbc].[dbo].[EarthquakeData];'''
            
    cursor.execute(Sql)

    input("\nPress return to continue")
    # Print out the cursor metadata for the last call
    try:
        allRows = cursor.fetchall()
    except pyodbc.Error as pyodbcError:
        print(f"Error: {str(pyodbcError)}")

    input("\nPress return to continue")

    # Define SQL BUT render point as a string 
    Sql = '''SELECT EarthquakeID, Earthquakeinformation.STAsText()
            FROM [djbpyodbc].[dbo].[EarthquakeData];'''

    cursor.execute(Sql)
       
    try:
        allRows = cursor.fetchall()
    except pyodbc.Error as pyodbcError:
        print(f"Error: {str(pyodbcError)}")
   
    printCursorResInfo(cursor)
    # print out the row
    for row in allRows:
            print(row)
            
    print("\n")
        