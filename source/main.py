from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, qApp, QMenuBar,QCheckBox
from PyQt5.QtWidgets import QFileDialog,QHBoxLayout, QComboBox, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import Qt,QtCore

from ScriptModel import ScriptModel
from DBManager import DBManager
from SpeechGenerator import SpeechGenerator

import sys, time 
from time import localtime, strftime
import sqlite3

# You should change two variables by your own AWS id/key values.
my_aws_id = "Your ID"
my_aws_key= "Your Key"

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.title = 'Speech Maker'
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 768    
        self.setWindowTitle(self.title)    
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.selectedRow = -1

        self.tableWidget = ScriptTableWidget()
        self.setCentralWidget(self.tableWidget)

        self.initMenuBar()
        self.statusBar().showMessage('')
       
    
    def initMenuBar(self):
        menubar = self.menuBar()

        # File Menu (load, exit)
        LoadAction = QAction('Load DB File', self)
        LoadAction.triggered.connect(self.tableWidget.loadDBFile)

        ExitAction = QAction('Exit', self)
        ExitAction.triggered.connect(qApp.quit)
   
        File = menubar.addMenu("File")        
        File.addAction(LoadAction)
        File.addAction(ExitAction)

        # Edit Menu (Create Database, Create New Table)
        NewDatabaseAction = QAction('Create Database',self)
        NewDatabaseAction.triggered.connect(self.tableWidget.createDatabase)

        ScenarioAction = QAction('Create New Table',self)
        ScenarioAction.triggered.connect(self.tableWidget.createDatabaseTable)
        
        EditMenu = menubar.addMenu('Edit')
        EditMenu.addAction(ScenarioAction)
        EditMenu.addAction(NewDatabaseAction)

        # Generate Menu (All, Current)

        GenCurrentTable = QAction('Current Table',self)
        GenCurrentTable.triggered.connect(self.tableWidget.generateCurrent)
        GenAllTables = QAction('All',self)
        GenAllTables.triggered.connect(self.tableWidget.generateAll)

        GenMenu = menubar.addMenu('Generate')
        GenMenu.addAction(GenCurrentTable)
        GenMenu.addAction(GenAllTables)

        # Help Menu (Nothing)
        HelpMenu = menubar.addMenu('Help')

        # Icon 
        AddAction = QAction(QIcon('icons/plus.png'),'Add', self)
        AddAction.triggered.connect(self.tableWidget.appendNewLine)        
        SubAction = QAction(QIcon('icons/minus.png'),'Delete', self)
        SubAction.triggered.connect(self.tableWidget.deleteLastLine)
        InsertAction = QAction(QIcon('icons/add.png'),'Insert', self)   
        InsertAction.triggered.connect(self.tableWidget.insertLine)     
        RemoveAction = QAction(QIcon('icons/remove.png'),'Remove', self)
        RemoveAction.triggered.connect(self.tableWidget.removeLine)
        UpdateAction = QAction(QIcon('icons/refresh.png'),'Update',self)
        #UpdateAction.triggered.connect(self.tableWidget.updateDB)
        UpdateAction.triggered.connect(self.tableWidget.updateDatabase)

        self.toolbar = self.addToolBar('Add')
        self.toolbar.addAction(AddAction)
        self.toolbar.addAction(SubAction)       
        self.toolbar.addAction(InsertAction)       
        self.toolbar.addAction(RemoveAction)
        self.toolbar.addAction(UpdateAction)


        #toolbar.addAction(AddAction)



class ScriptTableWidget(QWidget):

    ScenarioData = {}    
    PrevScenarioData = {}

    ScriptData = []

    def __init__(self):
        super().__init__()
        self.title = 'Generate Amazon Polly'
        self.left = 0
        self.top = 0
        self.width = 1400
        self.height = 768
        self.maxRow = 100
        self.defautlRow = 30 # display & editing
        self.numRow = 0 # current
        self.numCol = 10

        self.tableList = [] 
        self.currentTableName = None                
        self.database = None

        self.ScriptData.clear()

        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)        
        self.createTable()               

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout() 
                       
        # Add combox box to choose a table from database
        self.cbTable = QComboBox()
        self.layout.addWidget(self.cbTable)
        
        self.cbTable.activated[str].connect(self.changeTableName)

        self.layout.addWidget(self.tableWidget) 
        
        self.setLayout(self.layout) 

        # Show widget
        self.show()



    def createDatabase(self): # set database?
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", filter="db" ,options=options)
        print('Selected filename: ' + fileName+'.db')

        if fileName.find('.db') == -1:
            fileName = fileName + '.db'

        if len(fileName) > 0:             
            self.DBFileName = fileName
            self.database = DBManager(self.DBFileName)
            self.database.connect()    

    def createDatabaseTable(self): # new scenario
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter Scenario Title:')
        if ok:
            print(str(text))
            self.currentTableName = str(text) # change later!!!

        self.cbTable.addItem(text) # add item to combobox
        
        self.tableList.append(text) # add tableList

        self.ScenarioData[text] = []
        print(len(self.ScenarioData[text]))

    def generateCurrent(self): # amazon polly
        print("Generate Selected Scripts")
        id = my_aws_id
        key= my_aws_key
        # folder 
        # script
        
        # check selected item
        speech_lines = []
        speech_audio = []
        speech_marks = []        
        speech_wavs = []

        #speech_lines = [script["Text"] for script in self.ScenarioData]
        print(self.currentTableName)
        print(self.ScenarioData[self.currentTableName])
        print(self.ScenarioData[self.currentTableName][0].getData())
                
        rowNum = len(self.ScenarioData[self.currentTableName])
        print("row: ", rowNum)        
        for index in range(rowNum):            
            row = self.ScenarioData[self.currentTableName][index].getData()
            speech_lines.append(row["Text"])            
            speech_audio.append("../output/"+row["Audio"]+".mp3")
            speech_marks.append("../output/"+row["Audio"]+".marks")           
            speech_wavs.append("../output/"+row["Audio"])

        generator = SpeechGenerator(id,key)        
        generator.generate_audio_marks(speech_lines,speech_audio,speech_marks)             
        generator.conv_mp3_to_wav(speech_wavs)

    def generateAll(self): # amazon polly

        print("Generate All Scripts")
        id = my_aws_id
        key= my_aws_key
        speech_lines = []
        speech_audio = []
        speech_marks = []        
        speech_wavs = []
        print(self.tableList)
        for tablename in self.tableList:
            rowNum = len(self.ScenarioData[tablename])
            speech_lines = []
            speech_audio = []
            speech_marks = []
            speech_wavs = []
            for index in range(rowNum):
                row = self.ScenarioData[tablename][index].getData()
                speech_lines.append(row["Text"])            
                speech_audio.append("../output/"+row["Audio"]+".mp3")
                speech_marks.append("../output/"+row["Audio"]+".marks")           
                speech_wavs.append("../output/"+row["Audio"])

            generator = SpeechGenerator(id,key)        
            generator.generate_audio_marks(speech_lines,speech_audio,speech_marks)             
            generator.conv_mp3_to_wav(speech_wavs)

    # toolbar function
    def appendNewLine(self):       
        if self.currentTableName is not None:
            print('from',len(self.ScenarioData[self.currentTableName]))
            self.ScenarioData[self.currentTableName].append(ScriptModel())
            print('to',len(self.ScenarioData[self.currentTableName]))

            self.tableWidget.setRowCount(len(self.ScenarioData[self.currentTableName]))        
            self.tableWidget.setColumnCount(self.numCol)
        else: 
            QMessageBox.question(self, 'message', "No table, create one.", QMessageBox.Yes)

        #self.numRow += 1            
        
    
    def deleteLastLine(self):
        if self.currentTableName is not None:
            print('delete last line')
            print('from',len(self.ScenarioData[self.currentTableName]))
            print(len(self.ScenarioData[self.currentTableName]))
            
            if len(self.ScenarioData[self.currentTableName]) > 0:
                # delete last line
                self.ScenarioData[self.currentTableName] = self.ScenarioData[self.currentTableName][:-1]
            print('to',len(self.ScenarioData[self.currentTableName]))

            self.storeTable(self.currentTableName)

            self.tableWidget.setRowCount(len(self.ScenarioData[self.currentTableName]))        
            self.tableWidget.setColumnCount(self.numCol)
        else:
            QMessageBox.question(self, 'message', "No table, create one.", QMessageBox.Yes)

    def insertLine(self):
        print('insert line above selected row: ', self.selectedRow)          
        if self.currentTableName is None:
            print("no table name")
            return False

        # append new cell
        self.ScenarioData[self.currentTableName].append(ScriptModel())
        self.tableWidget.setRowCount(len(self.ScenarioData[self.currentTableName]))        
        self.tableWidget.setColumnCount(self.numCol)

        num = len(self.ScenarioData[self.currentTableName])            
        # for i in range(num):
        #     print(self.ScenarioData[self.currentTableName][i].getData())    
        
        for i in range(num-1, -1 ,-1):
            if i > self.selectedRow:                     
                data = self.ScenarioData[self.currentTableName][i-1].getData()
                #self.ScenarioData[self.currentTableName][i].copyData(self.ScenarioData[self.currentTableName][i-1])
                self.ScenarioData[self.currentTableName][i].copyData(data)
            if i == self.selectedRow:
                self.ScenarioData[self.currentTableName][i].clearData()                                    

        # renumber
        for i in range(num):
            self.ScenarioData[self.currentTableName][i].setScriptID(i+1)

        # for i in range(num):
        #     print(self.ScenarioData[self.currentTableName][i].getData())    

        self.tableWidget.clear()
        self.updateWidgetTable()

        return True


    def removeLine(self):
        print('remove selected row: ', self.selectedRow)
        if self.currentTableName is None:
            print("no table name")
            return False        

        num = len(self.ScenarioData[self.currentTableName])
        if num <= 0:
            print("no items to read")
            return  False

        if num > 1:                                                  
            for i in range(num-1):
                if i >= self.selectedRow:
                    # copy item from next
                    data = self.ScenarioData[self.currentTableName][i+1].getData()
                    self.ScenarioData[self.currentTableName][i].copyData(data)
                
        # last delete last item
        self.ScenarioData[self.currentTableName].pop(-1)

        # renumbering of ScriptID
        num_new = len(self.ScenarioData[self.currentTableName])
        for i in range(num_new):
            self.ScenarioData[self.currentTableName][i].setScriptID(i+1)

        # change the table widget
        self.tableWidget.setRowCount(len(self.ScenarioData[self.currentTableName]))        
        self.tableWidget.setColumnCount(self.numCol)            
        self.tableWidget.clear()
        self.updateWidgetTable()    

        # debug
        num = len(self.ScenarioData[self.currentTableName])
        for i in range(num):
             print(self.ScenarioData[self.currentTableName][i].getData())

        return True



    def updateDatabase(self):
        self.storeTable(self.currentTableName)    

        self.PrevTableList = []
        self.PrevScenarioData = {}
        self.PrevScenarioData.clear()
        # get table list from database
        self.PrevTableList = self.database.getTableList()       

        # get scenario data from database                
        for tableName in self.PrevTableList:
            records = self.database.fetchall(tableName)
            self.PrevScenarioData[tableName] = []
            for record in records:
                data = ScriptModel()
                data.setData(record)
                self.PrevScenarioData[tableName].append(data)
        
        # drop all tables inside database
        for tableName in self.PrevTableList:
            self.database.dropTable(tableName)        
        
        if len(self.PrevTableList) == 0: # there is no previous data (at first)
            # create all the table for storing ScenarioData
            time_update = self.getCurrentLocatTime()
            for tableName in self.tableList:
                self.database.createTable(tableName)                
                # insert all the current data into database
                num_record = len(self.ScenarioData[tableName])
                for index in range(num_record):                    
                    record = self.ScenarioData[tableName][index].getData()                
                    record["Date"] = time_update
                    self.ScenarioData[tableName][index].row["Date"] = time_update
                    # insert record into database
                    self.database.insertRecord(tableName,record)
        else:
            time_update = self.getCurrentLocatTime()
            for tableName in self.tableList:
                self.database.createTable(tableName)                
                if tableName in self.PrevScenarioData: # has_key                    
                    # check update contents
                    num_record = len(self.ScenarioData[tableName])                    
                    for index in range(num_record):
                        record = self.ScenarioData[tableName][index].getData()
                        match_index, update_result = self.isUpdated(record, self.PrevScenarioData[tableName])
                        if update_result == True:
                            record["Date"] = time_update
                            self.ScenarioData[tableName][index].row["Date"] = time_update
                        else:
                            record["Date"] = self.PrevScenarioData[tableName][match_index].row["Date"]                                                    
                            self.ScenarioData[tableName][index].row["Date"] = self.PrevScenarioData[tableName][match_index].row["Date"]                                                    
                        self.database.insertRecord(tableName,record)
                else:                                        
                    # insert all the current data into database
                    num_record = len(self.ScenarioData[tableName])
                    for index in range(num_record):                    
                        record = self.ScenarioData[tableName][index].getData()                
                        record["Date"] = time_update                        
                        self.database.insertRecord(tableName,record)

        # to display date field
        self.updateWidgetTable()    
            
    def isUpdated(self, record, previous_data):
        num_record = len(previous_data)
        for index in range(num_record):
            previous_record = previous_data[index].getData()
            matched = (record["Type"] == previous_record["Type"]) and \
                    (record["Text"] == previous_record["Text"]) and \
                    (record["FileName"] == previous_record["FileName"]) and \
                    (record["Audio"] == previous_record["Audio"]) and \
                    (record["Class1"] == previous_record["Class1"]) and \
                    (record["Class2"] == previous_record["Class2"]) and \
                    (record["Class3"] == previous_record["Class3"])
            if matched == True:
                return index, False
        return -1, True


        # delete table 기능이 필요하겠군(메뉴 중에)
        

    def getCurrentLocatTime(self):
        t_local = localtime(time.time())
        time_format = '%Y-%m-%d %H:%M:%S'
        time_str = strftime(time_format,t_local)
        return time_str
        
    def updateDB(self):                
        # check time
        self.storeTable(self.currentTableName)

        if self.database is not None:       
            TableNames = [self.cbTable.itemText(i) for i in range(self.cbTable.count())]
            for i in range(self.cbTable.count()):
                # get tableName from combobox
                tableName = self.cbTable.itemText(i)
                self.database.createTable(tableName)
                num_record = len(self.ScenarioData[tableName])
                for index in range(num_record):                    
                    record = self.ScenarioData[tableName][index].getData()
                    # insert record into database
                    self.database.insertRecord(tableName,record)                      
        else:
            QMessageBox.question(self, 'message', "No database, load or create one first", QMessageBox.Yes)


    def loadDBFile(self):
        # dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        # fileName include fullpath        
        self.DBFileName = fileName
        self.database = DBManager(self.DBFileName)
        # clear data
        self.ScenarioData.clear()
        # set table name into combobox
        self.setTableNames()
        # read selected files
        self.readDatabase()        
        # set table
        self.setWidgetTable()


    def readDatabase(self):             
        #self.database.connect()
        for tableName in self.tableList:
            records = self.database.fetchall(tableName)
            self.ScenarioData[tableName] = []            
            for record in records:
                data = ScriptModel()
                data.setData(record)
                self.ScenarioData[tableName].append(data)
                
    
        
    def changeTableName(self, text):  # when the combobox is chosen.
        # change table name
        print(text,'is chosen')      

        self.storeTable(self.currentTableName)

        self.currentTableName = text

        self.tableWidget.clear()

        self.updateWidgetTable()


    def storeTable(self,tableName):
        rowNum = len(self.ScenarioData[tableName])
        print("row: ", rowNum)
        for index in range(rowNum):
            scriptData = self.ScenarioData[tableName][index]            
            #for scriptData in self.ScenarioData[self.currentTableName]:
            # foreach table            
            rowData = [None]*10
            for  i in range(10):
                item = self.tableWidget.item(index,i)
                if item is not None:                    
                    rowData[i] = item.text()
                else:
                    print("not none")
                    rowData[i] = ""
            
            self.ScenarioData[tableName][index].setData(rowData)
            #scriptData.setData(rowData)         
                    


    def updateWidgetTable(self):        
        if len(self.ScenarioData[self.currentTableName]) > 0:
            num_row = len(self.ScenarioData[self.currentTableName])
            num_col = 10 #len(self.ScenarioData[self.currentTableName][0].keys())        
        else:
            num_row = 0
            num_col = 10
        
        self.tableWidget.setRowCount(len(self.ScenarioData[self.currentTableName]))        
        self.tableWidget.setColumnCount(self.numCol)
        self.tableWidget.setHorizontalHeaderLabels(["ScriptID","Type","Text","FileName","Audio","Class1","Class2","Class3","Description","Date"])

        for i in range(num_row):                      
            self.tableWidget.setItem(i,0,QTableWidgetItem(str(self.ScenarioData[self.currentTableName][i].row["ScriptID"])))
            self.tableWidget.setItem(i,1,QTableWidgetItem(self.ScenarioData[self.currentTableName][i].row["Type"]))
            self.tableWidget.setItem(i,2,QTableWidgetItem(self.ScenarioData[self.currentTableName][i].row["Text"]))
            self.tableWidget.setItem(i,3,QTableWidgetItem(self.ScenarioData[self.currentTableName][i].row["FileName"]))
            self.tableWidget.setItem(i,4,QTableWidgetItem(self.ScenarioData[self.currentTableName][i].row["Audio"]))            
            self.tableWidget.setItem(i,5,QTableWidgetItem(self.ScenarioData[self.currentTableName][i].row["Class1"]))
            self.tableWidget.setItem(i,6,QTableWidgetItem(self.ScenarioData[self.currentTableName][i].row["Class2"]))
            self.tableWidget.setItem(i,7,QTableWidgetItem(self.ScenarioData[self.currentTableName][i].row["Class3"]))
            self.tableWidget.setItem(i,8,QTableWidgetItem(self.ScenarioData[self.currentTableName][i].row["Description"]))            
            self.tableWidget.setItem(i,9,QTableWidgetItem(self.ScenarioData[self.currentTableName][i].row["Date"]))
        
        self.tableWidget.resizeColumnsToContents()
        #self.tableWidget.move(0,0)                

        # table selection change
        #self.tableWidget.doubleClicked.connect(self.on_click)     
        

    def createTable(self):  # make table at first (no line)
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.numRow)        
        self.tableWidget.setColumnCount(self.numCol)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(["ScriptID","Type","Text","FileName","Audio","Class1","Class2","Class3","Description","Date"])
        # self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))       
    
        for i in range(10):
            self.tableWidget.setColumnWidth(i,100)

        #self.tableWidget.resizeColumnsToContents()
        self.tableWidget.move(0,0)        

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    def setTableNames(self):
        self.tableList = self.database.getTableList()        
        for tableName in self.tableList:
            self.cbTable.addItem(tableName)

        if len(self.tableList) != 0:
            self.currentTableName = self.tableList[0]
        else:
            self.currentTableName = ""
            

    def setWidgetTable(self):        
        
        if len(self.tableList) > 0:
            #
            self.currentTableName = self.tableList[0]
            self.tableWidget.clear()        
            self.updateWidgetTable()
        else: 
            print("no table in the database")
            self.tableWidget.clear()
            self.tableWidget.setRowCount(len(self.ScenarioData[self.currentTableName]))        
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setHorizontalHeaderLabels(["ScriptID","Type","Text","FileName","Audio","Class1","Class2","Class3","Description","Date"])



    @pyqtSlot()
    def on_click(self):
        print("clicked...\n")            
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            #print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            self.selectedRow = currentQTableWidgetItem.row()
            print("row ", currentQTableWidgetItem.row(), " is selected.")

            
 
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    #ex = ScriptTableWiget()
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())      