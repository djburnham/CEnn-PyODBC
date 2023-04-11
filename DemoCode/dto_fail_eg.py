# Script to illustrate selecting a spatial type with no conversion  

import json
import pyodbc

import struct
from datetime import datetime, timedelta, timezone

def printCursorResInfo(cursor):
        print('\n**Result description from cursor**')
        for column in cursor.description:
                print('Name: ' + column[0])
                print('Python type: ' + str(column[1]))
                print('Nullable: ' + str(column[6]) + '\n')

# Define the function that the pyodbc module uses to convert datetime offsets
def handle_datetimeoffset(dto_value):
    # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 500000000, -6, 0)
    return datetime(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6] // 1000,
                    timezone(timedelta(hours=tup[7], minutes=tup[8])))                

# config file with access creds to the database
with open('DemoCode//config.json') as f:
    d = json.load(f)

hostname = d['hostname']
user     = d['username']
psw      = d['psw']
database = 'djbpyodbc'

connectString = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+\
hostname+';DATABASE='+database+';UID='+\
user+';PWD='+psw+';TrustServerCertificate=yes'

# We can use a python context manager with pyodbc.connect()
with  pyodbc.connect(connectString) as cnxn:
    # Create a cursor object from the connection
    cursor = cnxn.cursor()
    cursor.setinputsizes([(pyodbc.SQL_WVARCHAR, 50, 0)])
    
    # Select on a Date time Offset type in dto_test
    Sql = '''SELECT id, dto_col
            FROM [djbpyodbc].[dbo].[dto_test];'''
            
    cursor.execute(Sql)

    input("\nPress return to continue")
    # Print out the cursor metadata for the last call
    try:
        allRows = cursor.fetchall()
    except pyodbc.Error as pyodbcError:
        print(f"Error: {str(pyodbcError)}")

    input("\nPress return to continue")

    # register the date time offset convertor function with the CONNECTION
    cnxn.add_output_converter(-155, handle_datetimeoffset)

    # Re-execute the sql 
    cursor.execute(Sql)
       
    try:
        allRows = cursor.fetchall()
    except pyodbc.Error as pyodbcError:
        print(f"Error: {str(pyodbcError)}")
   
    printCursorResInfo(cursor)
    # print out the row
    for row in allRows:
            print(row)

    cnxn.clear_output_converters()            
    print("\n")
          