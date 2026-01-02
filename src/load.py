import pyodbc
import pandas as pd

def load_and_process_data_in_sql(cursor: pyodbc.Cursor, df_combined: pd.DataFrame):

    #truncate staging tables
    cursor.execute('TRUNCATE TABLE dbo.Tbl_Dashboard_Data_STAGING_Diagnostic_Waits')
    cursor.execute('truncate table dbo.Tbl_Dashboard_Data_STAGING')
    cursor.commit()

    #Insert into diagnostic waits staging table
    values = df_combined.itertuples(index=False, name= None)  #get iterator of tuples containing the data row by row. 1 tuple = 1 row

    cursor.executemany(
        "INSERT INTO dbo.Tbl_Dashboard_Data_STAGING_Diagnostic_Waits([Metric], [Date], [Value], [Source], [Identifier], [Identifier_Group]) "
        "values(?, ?, ?, ?, ?, ?) "
        ,values)
    cursor.commit()

    #Process data into main staging table
    cursor.execute('exec sp_dashboard_data_diagnostic_waits')
    cursor.commit()

    #Process from main staging table into reporting table
    cursor.execute('exec dbo.sp_dashboard_data_process_from_staging')
    cursor.commit()



def load(df: pd.DataFrame):

    with  pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=ServerName;"
        "DATABASE=DbName;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    ) as conn:
        
        cursor = conn.cursor()
        load_and_process_data_in_sql(cursor, df)
