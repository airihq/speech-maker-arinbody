
class ScriptModel:

    def __init__(self):
        self.row = {}
        
    def clearData(self):
        self.row["ScriptID"] = ""
        self.row["Type"] = ""
        self.row["Text"] = ""
        self.row["FileName"] = ""
        self.row["Audio"] = ""
        self.row["Class1"] = ""
        self.row["Class2"] = ""
        self.row["Class3"] = ""
        self.row["Description"] = ""
        self.row["Date"] = ""
        
    def copyData(self,sourceRow):
        self.row["ScriptID"] = sourceRow["ScriptID"]
        self.row["Type"] = sourceRow["Type"]
        self.row["Text"] = sourceRow["Text"]
        self.row["FileName"] = sourceRow["FileName"]
        self.row["Audio"] = sourceRow["Audio"]
        self.row["Class1"] = sourceRow["Class1"]
        self.row["Class2"] = sourceRow["Class2"]
        self.row["Class3"] = sourceRow["Class3"]
        self.row["Description"] = sourceRow["Description"]
        self.row["Date"] = sourceRow["Date"]

    def setData(self,row):
        self.row["ScriptID"] = row[0]
        self.row["Type"] = row[1]
        self.row["Text"] = row[2]
        self.row["FileName"] = row[3]
        self.row["Audio"] = row[4]
        self.row["Class1"] = row[5]
        self.row["Class2"] = row[6]
        self.row["Class3"] = row[7] 
        self.row["Description"] = row[8]
        self.row["Date"] = row[9]   

    def getData(self):
        return self.row
        
    def setScriptID(self,id):
        self.row["ScriptID"] = id
    