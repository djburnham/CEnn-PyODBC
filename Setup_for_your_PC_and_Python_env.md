### Setting up Your PC and Your Python Environment
1. Install the Microsoft ODBC Driver for Windows
    1. go to https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16
    2. click on the link "Download Microsoft ODBC Driver 18 for SQL Server (x64)" on the page 
    3. execute the downloaded msodbcsql.msi file as a system admin to install the driver 
    see [SQL Server ODBC Install Dialogue](Microsoft%20SQL%20Server%20ODBC%20Driver%20Install.pdf) for details

2. Create a virtual python environment and install the PyODBC module
```dos
C:\Users\DavidBurnham\temp>mkdir pyodbbc_wd
C:\Users\DavidBurnham\temp>cd pyodbbc_wd
C:\Users\DavidBurnham\temp\pyodbbc_wd>c:\Python311\python.exe -m venv .venv
C:\Users\DavidBurnham\temp\pyodbbc_wd>.venv\Scripts\activate.bat
(.venv) C:\Users\DavidBurnham\temp\pyodbbc_wd>pip install pyodbc
Collecting pyodbc
  Downloading pyodbc-4.0.35-cp311-cp311-win_amd64.whl (66 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 66.0/66.0 kB 1.7 MB/s eta 0:00:00
Installing collected packages: pyodbc
Successfully installed pyodbc-4.0.35

(.venv) C:\Users\DavidBurnham\temp\pyodbbc_wd>
```
3. Clone a copy of the demo files and exercise file 
```
C:\Users\DavidBurnham\temp> git clone https://github.com/djburnham/CEnn-PyODBC.git
```
4. Start Visual Studio Code from the directory created by the git clone operation
```
C:\Users\DavidBurnham\temp> cd CEnn-PyODBC
C:\Users\DavidBurnham\temp\CEnn-PyODBC> code .
```
5. Edit the config.json file in the DemoCode directory and replace the \<Directives\> in the file with your username and password for the SQL database you used earlier for SQL training.

<div style="page-break-after: always;"></div>

6. Load up the simple_dbc.py file in the editor - inspect it and check that it runs OK. You should get the current date and time for the database you have connected to, as shown below :
```
Connection Attributes
Autocommit = False
Timeout seconds = 0

('11 Apr 2023 10:46:24:720', )
```

If you have the Date and time returned to you you have successfully set up your PC and Python environment 
