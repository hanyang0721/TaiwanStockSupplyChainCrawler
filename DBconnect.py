# coding=utf-8
import pyodbc



class DBconnect:
    def __init__(self, addr, database, username, password):
        self.Server = {"server": addr, "database": database, "username": username, 'password': password}
        self.conn = None
        self.driver = '{SQL Server Native Client 11.0}'

    def Connect(self):
        self.conn = pyodbc.connect('DRIVER=' + self.driver + ';SERVER=' + self.Server['server'] + ';DATABASE=' + self.Server['database'] + ';UID=' + self.Server['username'] + ';PWD=' + self.Server['password'])

    def InsertStockCategory(self, category, stockname, stockidx):
        cursor = self.conn.cursor()
        SQL = " INSERT INTO dbo.tblStockCategory([categoryname],[Stockname],[Stockid]) values (? , ?, ?) "
        param_values = [category, stockname, stockidx]
        cursor.execute(SQL, param_values)
        cursor.commit()
