from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
import mysql.connector
from mysql.connector import errorcode

class Digest(QDialog):
    connectconfig = {'user':'root', 'password':'Silver.pass1', 'host':'localhost', 'database':'calories'}

    def __init__(self, U_ID):
        super(Digest,self).__init__()
        loadUi('ui/editUI.ui',self)
        pixmap = QPixmap('others/down-arrow.png')
        self.label_12.setPixmap(pixmap)

        self.setWindowTitle("Entries")
        
        #Combobox present on forms
        self.Mfillcombobox()
        self.cboMECode.currentTextChanged.connect(self.Mcombobox_changed)

        #Buttons present on forms
        self.searchMButton.clicked.connect (self.MSearchButton_clicked)
        self.addEMButton.clicked.connect(self.MAddButton_clicked)
        self.delEMButton.clicked.connect(self.MDeleteButton_clicked)
        self.editEMButton.clicked.connect(self.MEditButton_clicked)
        self.backEButton.clicked.connect(self.exit_dialog)
        
    def Mfillcombobox(self):
        #Connect to MySQL
        cnx = mysql.connector.connect(**self.connectconfig)
        cursor = cnx.cursor()
        cursor.execute("Select * From tblMeal")
        self.cboMECode.clear()
        self.cboMECode.addItem("-Meal Code-")

        for row in cursor:
            self.cboMECode.addItem(row[0])
        
        #Close the cursor & connection
        cursor.close()
        cnx.close()
        
    def Mcombobox_changed(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            code = self.cboMECode.currentText()

            # Search Meal based on combobox
            cursor.execute("Select * From tblMeal Where M_ID = '%s'" % code)
            row = cursor.fetchone()
            if row is not None:
                self.leMECode.setText(str(row[0]))
                self.leMEName.setText(str(row[1]))
                self.leNCal.setText(str(row[2]))
                self.leNPro.setText(str(row[3]))
                self.leNCarbs.setText(str(row[4]))
                
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the connection")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:   
                print(err)
        else:
            cursor.close()
            cnx.close()

    def MSearchButton_clicked(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            code = self.leMECode.text ()

            # Search Meal
            cursor.execute("Select * From tblMeal Where M_ID = '%s'" % code)
            row = cursor.fetchone()
            if row is not None:
                self.leMEName.setText(str(row[1]))
                self.leNCal.setText(str(row[2]))
                self.leNPro.setText(str(row[3]))
                self.leNCarbs.setText(str(row[4]))
            else:
                self.leMEName.setText("")
                self.leNCal.setText("")
                self.leNPro.setText("")
                self.leNCarbs.setText("")

                QMessageBox.about(self, "Meal", "Meal Not Found")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the connection")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:   
                print(err)
        else:
            cursor.close()
            cnx.close()
 
    def MAddButton_clicked(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            code = self.leMECode.text()
            name = self.leMEName.text()
            calories = self.leNCal.text()
            proteins = self.leNPro.text()
            carbs = self.leNCarbs.text()

            #Validations of inputs
            if not code or not name:
                QMessageBox.warning(self, "Warning", "Please fill in all fields.")
                return

            #Validation if meal already exist.
            cursor.execute("SELECT * FROM tblMeal WHERE M_ID = %s", (code,))
            w_record = cursor.fetchone()
            if w_record:
                QMessageBox.warning(self, "Add a Meal", "Warning, M_ID already exist.\nPlease try again")
            else:
                #insert new meal
                cursor.execute("Insert Into tblMeal (M_ID, M_Name, N_Calories, N_Protein, N_Carbs) Values (%s, %s, %s, %s, %s)", (code, name, calories, proteins, carbs))
                cnx.commit()

                QMessageBox.information(self, "Added", "Successfully added a meal.")

                self.Mfillcombobox()

                self.leMECode.setText("")
                self.leMEName.setText("")
                self.leNCal.setText("")
                self.leNPro.setText("")
                self.leNCarbs.setText("")
                
                listTableRecords = ListTable()
                

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the connection")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:   
                print(err)
        else:
            cursor.close()
            cnx.close()

    def MDeleteButton_clicked(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            code = self.leMECode.text()
            name = self.leMEName.text()
            calo = self.leNCal.text()
            pro = self.leNPro.text()
            carb = self.leNCarbs.text()
            
            #Validation of inputs
            if not code or not name:
                QMessageBox.warning(self, "Warning", "Please fill in all fields.")
                return

            #Validation if meal does not exist
            cursor.execute("SELECT M_ID FROM tblMeal WHERE M_ID = %s", (code,))
            w_record = cursor.fetchone()
            if not w_record:
                QMessageBox.warning(self, "Delete", "Warning, M_ID does not exist.\nPlease try again")
                return

            reply = QMessageBox.question(self, "Delete", "Do you want to delete this record?\n This will affect your own journal")
            if reply == QMessageBox.StandardButton.Yes:
                cursor = cnx.cursor()
                code = self.leMECode.text()
                cursor.execute("Delete From tblNutrients Where M_ID = '%s'" % code)
                cursor.execute("Delete From tblMeal Where M_ID = '%s'" % code)
                cnx.commit()

                self.leMECode.setText("")
                self.leMEName.setText("")
                self.leNCal.setText("")
                self.leNPro.setText("")
                self.leNCarbs.setText("")
                
                self.Mfillcombobox()

                listTableRecords = ListTable()
                listTableRecords.update_record()
            
            else:
                return
                
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the connection")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:   
                print(err)
        else:
           cursor.close()
           cnx.close()

    def MEditButton_clicked(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            code = self.leMECode.text()
            name = self.leMEName.text()
            calories = self.leNCal.text()
            proteins = self.leNPro.text()
            carbs = self.leNCarbs.text()
            
            #Validation of inputs
            if not code or not name:
                QMessageBox.warning(self, "Warning", "Please fill in all fields.")
                return

            #Validation if meal does not exist
            cursor.execute("SELECT M_ID FROM tblMeal WHERE M_ID = %s", (code,))
            w_record = cursor.fetchone()
            if not w_record:
                QMessageBox.warning(self, "Edit", "Warning, M_ID does not exist.\nPlease try again")
                return

            reply = QMessageBox.question(self, "Edit", "Do you want to edit this record?")
            if reply == QMessageBox.StandardButton.Yes:
                sql = "Update tblMeal Set M_Name  = '%s', N_Calories = '%s', N_Protein = '%s', N_Carbs = '%s'  Where M_ID = '%s'" % (name, calories, proteins, carbs, code)
                cursor.execute(sql)
                cnx.commit()

                self.leMECode.setText("")
                self.leMEName.setText("")
                self.leNCal.setText("")
                self.leNPro.setText("")
                self.leNCarbs.setText("")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the connection")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:   
                print(err)
        else:
            cursor.close()
            cnx.close()

    def exit_dialog(self):
        self.reject()


class ListTable (QDialog):
    connectconfig = {'user':'root', 'password':'Silver.pass1', 'host':'localhost', 'database':'calories'}

    def __init__(self):
        super(ListTable, self).__init__()
        loadUi('ui/mainRecordsUI.ui',self)

        self.tableLRecord.setHorizontalHeaderLabels(["ID", "Meal", "Calories (kcal)", "Proteins (grams)", "Carbohydrates(grams)"])
        self.update_record()

        self.backEButton.clicked.connect(self.exit_dialog)


    def update_record(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
        except mysql.connector.Error as err:
            print("Error connecting to database:", err)
            return

        query = "SELECT * FROM tblMeal;"
        try:
            cursor = cnx.cursor()
            cursor.execute(query)
        except mysql.connector.Error as err:
            print("Error executing query:", err)
            cnx.close()
            return

        self.tableLRecord.setRowCount(0)
        for row in cursor:
            rowPosition = self.tableLRecord.rowCount()
            self.tableLRecord.insertRow(rowPosition)
            for col, value in enumerate(row):
                self.tableLRecord.setItem(rowPosition, col, QTableWidgetItem(str(value)))

        #spacing of columns
        self.tableLRecord.setColumnWidth(0, 80)  
        self.tableLRecord.setColumnWidth(1, 173) 
        self.tableLRecord.setColumnWidth(2, 100) 
        self.tableLRecord.setColumnWidth(3, 100)
        self.tableLRecord.setColumnWidth(4, 150)

        cnx.close()

        #updating table
        self.tableLRecord.update() 
        self.tableLRecord.repaint()

    def exit_dialog(self):
        self.reject()
        
