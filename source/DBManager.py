import sqlite3

class DBManager:

    def __init__(self, dbFile):
        # do nothing        
        self.dbfile = dbFile
    
    def connect(self):
        self.conn = sqlite3.connect(self.dbfile)
        self.conn.close()

    def fetchall(self, tableName):                
        
        conn = sqlite3.connect(self.dbfile)
        cursor = conn.cursor()
        sql = "select * from " + tableName
        cursor.execute(sql)
        rows = cursor.fetchall()        
        conn.close()

        return rows
    
    # create table
    def createTable(self,tableName):
        try:
            conn = sqlite3.connect(self.dbfile)
            cursor = conn.cursor()
            sql = 'CREATE TABLE if not exists {}(ScriptID integer, Type text, Text text, FileName text, Audio text, Class1 text, Class2 text, Class3 text, Description text, Date text)'.format(tableName)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()                        
        except:                
            print("create table error")

    def dropTable(self,tableName):
        try:
            conn = sqlite3.connect(self.dbfile)
            cursor = conn.cursor()            
            sql = 'drop table if exists {}'.format(tableName)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
        except:
            print("drop error")
    
    def insertRecord(self,tableName,record):

        print(record)        
        try:
            conn = sqlite3.connect(self.dbfile)
            cursor = conn.cursor()            
            sql = 'INSERT INTO {}(ScriptID, Type, Text, FileName, Audio, Class1, Class2, Class3, Description, Date) \
                   VALUES({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'\
                   .format(tableName,record["ScriptID"],record["Type"],record["Text"],record["FileName"],record["Audio"],\
                   record["Class1"],record["Class2"],record["Class3"],record["Description"],record["Date"])
            print(sql)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
        except:
            print("insert error")


    # add rows / add row
    

    
    def getTableList(self):
        conn = sqlite3.connect(self.dbfile)
        sql = "select name from sqlite_master where type='table'"
        cursor = conn.cursor()
        cursor.execute(sql)
        List = cursor.fetchall()
        conn.close()
        tableList = []                        
        for item in List:
             tableList.append(item[0])
        return tableList
        
    
    
