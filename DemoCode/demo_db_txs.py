# Script to illustrate connection.autocommit mode 
import pyodbc
import json

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
    # Create a cursor object from the connection
    cursor = cnxn.cursor()
    cursor.setinputsizes([(pyodbc.SQL_WVARCHAR, 50, 0)])
    #autocommit False by default
    print(f"Autocommit is {str(cnxn.autocommit)}\n")
    
    # Create a new table with special offer items in it 
    cr_tab = '''CREATE TABLE [production].[promo_products](
	[promo_id] [int] IDENTITY(1,1) NOT NULL,
	[product_id] [int] NOT NULL,
	[product_name] [varchar](255) NOT NULL,
	[brand_id] [int] NOT NULL,
	[category_id] [int] NOT NULL,
	[model_year] [smallint] NOT NULL,
	[list_price] [decimal](10, 2) NOT NULL,
    PRIMARY KEY CLUSTERED 
    (
	    [product_id] ASC
    )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, 
    IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, 
    OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
    ) ON [PRIMARY];
    '''
    # Add all of the bikes for Surly  brand_id = 8 
    pop_tab = '''
    INSERT INTO [production].[promo_products]
    SELECT [product_id], [product_name], [brand_id], [category_id], [model_year], [list_price]
    FROM [production].[products]
    WHERE [brand_id]  = 8 ;
    '''       
    # Run the SQL and show what transactions we have open  
    # and what locks we have open
    input("\nAbout to CREATE TABLE Press return to continue")
    cursor.execute(cr_tab)
    input("\nAbout to Populate Table Press return to continue")
    cursor.execute(pop_tab) 

    input("\nAbout to Rollback Press return to continue")
    cnxn.rollback()

 
    input("\nPost rollback - set autocommit True - Press return to continue")

    # set the connection autocommit to True 
    cnxn.autocommit = True

    # Run the SQL again and see what transactions are active 
    # and what locks we have 
    print(f"Autocommit is {str(cnxn.autocommit)}\n")
    input("\nAbout to create table. Press return to continue")
    cursor.execute(cr_tab)
    input("\nAbout to populate table Press return to continue")
    cursor.execute(pop_tab)   
    input("\nAbout to Rollback Press return to continue")
    cnxn.rollback()
    input("\nAbout to DROP table Press return to continue")

    # Drop the table and see if we can roll that back 
    cursor.execute("DROP TABLE [production].[promo_products];")
    input("\nAbout to Rollback Press return to continue")
    cnxn.rollback()
    input("\nPress return to End")
    
    
          