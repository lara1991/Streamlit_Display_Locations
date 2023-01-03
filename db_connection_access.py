import pyodbc
import pandas as pd
    
class Database:
    def __init__(self,database_path):
        self.database_path = database_path
        self.conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+self.database_path+';')
        self.cursor = self.conn.cursor()
    
    def get_available_ms_access_drivers(self):
        lst_acc_db = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
        if len(lst_acc_db) > 0:
            print(lst_acc_db)
        else:
            print("Microsoft Access Driver - Not Found")
    
    def get_table_names(self):
        for row in self.cursor.tables():
            if not "MSys" in str(row.table_name):
                print(row.table_name)
    
    def get_column_names(self,table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        col_names = [col[0] for col in self.cursor.description]
        return col_names
    
    def search_and_get_data(self,sql_query,params=None):
        df = pd.read_sql_query(sql=sql_query,con=self.conn,params=params)
        return df

def main():
    db_path = "<path for database>"
    db = Database(database_path=db_path)
    # print(db.get_table_names())
    # print(db.get_column_names(table_name="Factory"))
    q = 'select * from sbu'
    df = db.search_and_get_data(sql_query=q)
    df = df[['SBUCode','CompName','Address']]
    print(df.head())
    
    
if __name__ == '__main__':
    main()
    
        
        
