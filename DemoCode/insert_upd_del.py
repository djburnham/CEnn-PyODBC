# Script to  

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
database = 'djbpyodbc'

connectString = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+\
hostname+';DATABASE='+database+';UID='+\
user+';PWD='+psw+';TrustServerCertificate=yes'

# We can use a python context manager with pyodbc.connect()
with  pyodbc.connect(connectString) as cnxn:
    # Set autocommit to on - talk about this later
    cnxn.autocommit = True
    # Create a cursor object from the connection
    cursor = cnxn.cursor()
    cursor.setinputsizes([(pyodbc.SQL_WVARCHAR, 50, 0)])
 
    Sql = '''SELECT car_id, manufacturer, model, fuel, engine_capacity, 
        engine_power FROM [dbo].[cars]; '''

    cursor.execute(Sql)
 
    # Print out the cursor metadata for the last call
    printCursorResInfo(cursor)
    
    allRows = cursor.fetchall()
    for row in allRows:
        print(row)   
        
    input("\nPress return to continue")

    Sql = '''INSERT INTO [dbo].[cars]
    (car_id, manufacturer, model, fuel, engine_capacity,engine_power)
    VALUES (?, ?, ?, ?, ?, ?) ; '''

    newCar1 = (8, 'Skoda', 'Submariner', 'Petrol', 2498, 220)
    newCar2 = (9,  'Saab', 'Talladega', 'Petrol', 1948, 197)

    for iCar in [newCar1, newCar2]:
        cursor.execute(Sql, iCar[0], iCar[1], iCar[2], iCar[3], iCar[4], iCar[5])
        print(f"Number of rows ins/upd/del in last call = {cursor.rowcount}")
    #        
    Sql = '''SELECT car_id, manufacturer, model, fuel, engine_capacity, 
             engine_power FROM [dbo].[cars]; '''

    cursor.execute(Sql)

    allRows = cursor.fetchall()
    for row in allRows:
        print(row) 

    input("\nPress return to continue")
    #
    Sql = ''' UPDATE [dbo].[cars] SET fuel = 'Electricity'
              WHERE car_id = ?; ''' 

    cursor.execute(Sql, 4)
    print(f"Number of rows ins/upd/del in last call = {cursor.rowcount}")
    #
    Sql = '''SELECT car_id, manufacturer, model, fuel, engine_capacity, 
             engine_power FROM [dbo].[cars]; '''

    cursor.execute(Sql)

    allRows = cursor.fetchall()
    for row in allRows:
        print(row)
    #
    input("\nPress return to continue")   
    #
    Sql = '''DELETE from [dbo].[cars]
              WHERE car_id = ?
              OR car_id = ?; '''

    cursor.execute(Sql, 8, 9)
    print(f"Number of rows ins/upd/del in last call = {cursor.rowcount}")

    #
    Sql = '''SELECT car_id, manufacturer, model, fuel, engine_capacity, 
             engine_power FROM [dbo].[cars]; '''
    
    cursor.execute(Sql)

    allRows = cursor.fetchall()
    for row in allRows:
        print(row)
    #
    input("\nPress return to continue")
    # clean up 
    cursor.execute('UPDATE [dbo].[cars] SET fuel=\'Electrickery\' WHERE car_id=4') 

