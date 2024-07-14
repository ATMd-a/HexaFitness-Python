import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
import mysql.connector
from mysql.connector import errorcode
from GlobalRecords import Digest, ListTable


class DashMenu (QMainWindow):
    connectconfig = {'user':'root', 'password':'Silver.pass1', 'host':'localhost', 'database':'calories'}

    def __init__(self, U_ID):
        super().__init__()
        loadUi('ui/MWindowUI.ui', self)
        self.U_ID = U_ID

        self.setWindowTitle("HexaFitness App")
        self.editButton.clicked.connect(lambda: self.editButton.toggle()) 

        #Buttons present on forms
        self.addMButton.clicked.connect(self.add_cals)
        self.recordButton.clicked.connect(self.rec_main)
        self.editButton.clicked.connect(self.edit_ent)
        self.refreshButton.clicked.connect(self.refresh_but)
        self.clearMButton.clicked.connect(self.clearM_but)
        self.clearXButton.clicked.connect(self.clearX_but)
        self.accountButton.clicked.connect(self.account_user)

        #headers of meals and exercise records
        self.tableXRecord.setHorizontalHeaderLabels(["Exercise", "Duration", "Burned Calories"])
        self.Xupdate_record()
        self.tableXMRecord.setHorizontalHeaderLabels(["Time", "Meal", "Serving", "Calories", "Protein", "Carbs"])
        self.XMupdate_record()
 
        #setting username and weight information
        username, weight = self.get_user_info(U_ID)
        self.username_label.setText(f"Hello {username}")
        self.wytLbl.setText(f"{weight}")
        self.weight = weight

        #qlabels that are updating
        self.numCal = self.findChild(QLabel, 'numCal')
        self.get_calorie()
        self.numPro = self.findChild(QLabel, 'numPro')
        self.get_protein()
        self.numCarb = self.findChild(QLabel, 'numCarb')
        self.get_carbs()
        self.numCB = self.findChild(QLabel, 'numCB')
        self.get_bcal()
        self.numDur = self.findChild(QLabel, 'numDur')
        self.get_duration()
        self.wytLblafter = self.findChild(QLabel, 'wytLblafter')
        self.resultweyt()
        self.lelost = self.findChild(QLabel, 'lelost')
        self.lostweyt()

    #display of total calories
    def get_calorie(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()

            query = """SELECT ROUND(SUM(tblMeal.N_Calories * User_Journal.M_Serving), 2) 
                        FROM User_Journal 
                        INNER JOIN tblMeal ON User_Journal.M_JID = tblMeal.M_ID 
                        WHERE User_Journal.U_ID = %s"""

            cursor.execute(query, (self.U_ID,))
            total_calories = cursor.fetchone()[0]

            if total_calories is None:
                total_calories = 0.00 

            self.numCal.setText(str(format(total_calories, '.2f')))

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

    #display of total protein
    def get_protein(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()

            query = """SELECT ROUND(SUM(tblMeal.N_Protein * User_Journal.M_Serving), 2) 
                        FROM User_Journal 
                        INNER JOIN tblMeal ON User_Journal.M_JID = tblMeal.M_ID 
                        WHERE User_Journal.U_ID = %s"""

            cursor.execute(query, (self.U_ID,))
            total_protein = cursor.fetchone()[0]

            if total_protein is None:
                total_protein = 0.00

            self.numPro.setText(str(format(total_protein, '.2f')))

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

    #display of total carbs
    def get_carbs(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()

            query = """SELECT ROUND(SUM(tblMeal.N_Carbs * User_Journal.M_Serving), 2) 
                        FROM User_Journal 
                        INNER JOIN tblMeal ON User_Journal.M_JID = tblMeal.M_ID 
                        WHERE User_Journal.U_ID = %s"""

            cursor.execute(query, (self.U_ID,))
            total_carb = cursor.fetchone()[0]

            if total_carb is None:
                total_carb = 0.00

            self.numCarb.setText(str(format(total_carb, '.2f')))

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

    #display of burned calories
    def get_bcal(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()

            query = """SELECT ROUND(SUM(CAST(E_CBurned AS DECIMAL(10,2))), 2) 
                        FROM tblExercise 
                        WHERE U_ID = %s"""

            cursor.execute(query, (self.U_ID,))
            total_bcal = cursor.fetchone()[0]

            if total_bcal is None:
                total_bcal = 0.00 

            self.numCB.setText(str(format(total_bcal, '.2f')))

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

    #display of total minutes of exercise
    def get_duration(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()

            query = """SELECT SUM(CAST(E_Duration AS UNSIGNED))
                        FROM tblExercise 
                        WHERE U_ID = %s"""

            cursor.execute(query, (self.U_ID,))
            total_dur = cursor.fetchone()[0]

            if total_dur is None:
                total_dur = 0.00

            self.numDur.setText(str(format(total_dur)))

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

    #display of "after" weight
    def resultweyt(self):
        #setting variables
        total_calories = float(self.numCal.text()) 
        total_burned_calories = float(self.numCB.text()) 

        #computation
        calorie_difference = total_calories - total_burned_calories

        result = str(round(float(self.weight) + (calorie_difference / 7700), 2))
        
        self.wytLblafter.setText(result)

    #display of the number of lost weight
    def lostweyt(self):
        #setting variable
        lostkg = float(self.wytLblafter.text())
        current_weight = float(self.weight)

        #computation
        result = str(round(current_weight - lostkg, 2))
        self.lelost.setText(result)

    #getting user info
    def get_user_info(self, U_ID):
        try:
            connection = mysql.connector.connect(**self.connectconfig)
            cursor = connection.cursor()

            query = "SELECT U_ID, U_Weight from tblUser WHERE U_ID = %s"
            cursor.execute(query, (U_ID,))
            result =cursor.fetchone()
            
            if result:
                return result[0], result[1]
            else:
                return "Unknown", "Unknown"
        except mysql.connector.Error as err:
            print("Error", err)
            return "Unknown1"




    #My Jounal button
    def add_cals(self):
        userw = self.get_user_info(self.U_ID)
        weight = userw[1]
        pdialog = Journal(weight, self.U_ID)
        pdialog.move(505,148)
        pdialog.exec()
  
    #List of Meals button
    def rec_main(self):
        pdialog = ListTable()
        pdialog.move(505,148)
        pdialog.exec()

    #Modify meals buttons
    def edit_ent(self):
        pdialog = Digest(self.U_ID)
        pdialog.move(505,148)
        pdialog.exec()

    #My account button
    def account_user(self):
        pdialog = Account(self.weight, self.U_ID)
        pdialog.move(505,148)
        pdialog.exec()





    #records of exercise of the user
    def Xupdate_record(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            query = "SELECT E_Name, E_Duration, E_CBurned FROM tblExercise WHERE U_ID = %s;"
            cursor = cnx.cursor()
            cursor.execute(query, (self.U_ID,))

            self.tableXRecord.setRowCount(0)
            for row in cursor:
                rowPosition = self.tableXRecord.rowCount()
                self.tableXRecord.insertRow(rowPosition)
                for col, value in enumerate(row):
                    self.tableXRecord.setItem(rowPosition, col, QTableWidgetItem(str(value)))

            #spacing of columns
            self.tableXRecord.setColumnWidth(0, 80) 
            self.tableXRecord.setColumnWidth(1, 70) 
            self.tableXRecord.setColumnWidth(2, 99)  

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

    #records of meal of the user
    def XMupdate_record(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()

            query = """SELECT M_Time, M_Name, M_Serving, N_Calories, N_Protein, N_Carbs 
                FROM User_Journal 
                INNER JOIN tblMeal ON User_Journal.M_JID = tblMeal.M_ID 
                WHERE User_Journal.U_ID = %s
                ORDER BY CASE M_Time
                    WHEN 'Breakfast' THEN 1
                    WHEN 'Lunch' THEN 2
                    WHEN 'Dinner' THEN 3
                    WHEN 'Snacks' THEN 4
                    ELSE 5
                END"""

            cursor.execute(query, (self.U_ID,))

            self.tableXMRecord.setRowCount(0)
            for row in cursor:
                rowPosition = self.tableXMRecord.rowCount()
                self.tableXMRecord.insertRow(rowPosition)
                for col, value in enumerate(row):
                    self.tableXMRecord.setItem(rowPosition, col, QTableWidgetItem(str(value)))

            #spacing of columns
            self.tableXMRecord.setColumnWidth(0, 80)
            self.tableXMRecord.setColumnWidth(1, 70)
            self.tableXMRecord.setColumnWidth(2, 50) 
            self.tableXMRecord.setColumnWidth(3, 50)
            self.tableXMRecord.setColumnWidth(4, 50)
            self.tableXMRecord.setColumnWidth(5, 50)

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

    #refresh button for info on dashboard
    def refresh_but(self):
        self.Xupdate_record()
        self.XMupdate_record()
        self.get_calorie()
        self.get_protein()
        self.get_carbs() 
        self.get_bcal() 
        self.get_duration()
        self.resultweyt()
        self.lostweyt()

        #info of updated weiht in my account
        username, weight = self.get_user_info(self.U_ID)
        self.username_label.setText(f"Hello {username}")
        self.wytLbl.setText(f"{weight}")
        self.weight = weight

    #clearing records on users meals
    def clearM_but(self):
        cnx = mysql.connector.connect(**self.connectconfig)
        cursor = cnx.cursor()

        # clearing records for meal on dashboard
        delete_query = "DELETE FROM User_Journal WHERE U_ID = %s"
        cursor.execute(delete_query, (self.U_ID,))
        cnx.commit()

        #updating table
        self.XMupdate_record()

    #clearing records on users exercise
    def clearX_but(self):
        cnx = mysql.connector.connect(**self.connectconfig)
        cursor = cnx.cursor()

        # clearing records for exercise on dashboard
        delete_query = "DELETE FROM tblExercise WHERE U_ID = %s"
        cursor.execute(delete_query, (self.U_ID,))
        cnx.commit()

        #updating table
        self.Xupdate_record()
  
#users journal
class Journal(QDialog):
    connectconfig = {'user':'root', 'password':'Silver.pass1', 'host':'localhost', 'database':'calories'}

    def __init__(self, weight, U_ID):
        super(Journal,self).__init__()
        loadUi('ui/journalUI.ui',self)
        pixmap = QPixmap('others/down-arrow.png')
        self.label_36.setPixmap(pixmap)
        self.label_27.setPixmap(pixmap)
        self.label_28.setPixmap(pixmap)

        self.setWindowTitle("Journal")
        self.weight = weight
        self.U_ID = U_ID

        #Exercise buttons
        self.calcuButton.clicked.connect(self.calculate_cal)
        self.addExButton.clicked.connect(self.XAddButton_clicked)

        self.MAfillcombobox()

        #Meals buttons
        self.cboAMCode.currentTextChanged.connect(self.MAcombobox_changed)
        self.addAMButton.clicked.connect(self.MAXddButton_clicked)

        self.backButton.clicked.connect(self.exit_dialog)
        
        #setting some lineedits for read only
        self.leExBurn.setReadOnly(True)
        self.leAMName.setReadOnly(True)
        self.leANCal.setReadOnly(True)
        self.leANPro.setReadOnly(True)
        self.leANCarb.setReadOnly(True)

    #calculation of burned calories
    def calculate_cal(self):
        xercise = self.cboExName.currentText()
        dur = self.leExDur.text()

        if not xercise or not dur:
            QMessageBox.warning(self, "Warning", "Please fill in both Exercise and Duration fields.")
            return       

        MET_values = {
            "Jogging": 7,
            "Jumping Rope": 11.8,
            "Cycling": 7.5,
            "Walking": 3.5,
            "Running": 8,
            "Yoga": 2.8, 
            "Dancing": 7.8,
            "Basketball": 6.5,
            "Volleyball": 4,
            "Boxing": 7.8,
        }

        if xercise in MET_values:
            MET = MET_values[xercise]
            #using int for getting the rounded number
            calories_burned = int(( MET * float(self.weight) * 3.5) / 200 * int(dur))

            self.leExBurn.setText(str(calories_burned))
            self.leExBurn.setReadOnly(True)

        else:
            self.leExBurn.setText("No")

    def XAddButton_clicked(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            xercise = self.cboExName.currentText()
            dur = self.leExDur.text()
            burnc = self.leExBurn.text()

            #validation od inputs
            if not xercise or not dur or not burnc:
                QMessageBox.warning(self, "Warning", "Please fill in both Exercise and Duration fields.")
                return   

            # Insert new user's ecervise
            cursor.execute("Insert Into tblExercise (U_ID, E_Name, E_Duration, E_CBurned) Values (%s, %s, %s, %s)", (self.U_ID, xercise, dur, burnc))
            cnx.commit()

            QMessageBox.information(self, "Added", "Successfully added a exercise.")

            self.leExDur.setText("")
            self.leExBurn.setText("")
                
            listTableRecords = DashMenu(self.U_ID)
            listTableRecords.Xupdate_record()

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

    def MAfillcombobox(self):
        cnx = mysql.connector.connect(**self.connectconfig)
        cursor = cnx.cursor()
        cursor.execute("Select * From tblMeal")
        self.cboAMCode.clear()
        self.cboAMCode.addItem("-Meal Code-")

        for row in cursor:
            self.cboAMCode.addItem(row[0])
        
        cursor.close()
        cnx.close()

    def MAcombobox_changed(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            code = self.cboAMCode.currentText()

            # Search available meals
            query = "SELECT * FROM tblMeal WHERE tblMeal.M_ID = %s;"
            cursor.execute(query, (code,))

            row = cursor.fetchone()
            if row is not None:
                self.leAMName.setText(str(row[1]))
                self.leANCal.setText(str(row[2]))
                self.leANPro.setText(str(row[3]))
                self.leANCarb.setText(str(row[4]))
                
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

    def MAXddButton_clicked(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            code = self.cboAMCode.currentText()
            name = self.leAMName.text()
            time = self.cboAMTime.currentText()
            serv = self.leAMServ.text()

            if not time or not serv:
                QMessageBox.warning(self, "Warning", "Please fill both time and # of serving fields.")
                return

            # Insert new user's meal
            cursor.execute("INSERT INTO User_Journal (U_ID, M_JID, M_Time, M_Serving) VALUES (%s, %s, %s, %s)", (self.U_ID, code, time, serv))
            cnx.commit()

            QMessageBox.information(self, "Added", "Successfully added a meal.")

            self.MAfillcombobox()

            self.leAMName.setText("")
            self.leAMServ.setText("")
            self.leANCal.setText("")
            self.leANPro.setText("")
            self.leANCarb.setText("")
                
            listTableRecords = DashMenu(self.U_ID)
            listTableRecords.XMupdate_record()

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

#users account
class Account(QDialog):
    connectconfig = {'user':'root', 'password':'Silver.pass1', 'host':'localhost', 'database':'calories'}

    def __init__(self, weight, U_ID):
        super(Account,self).__init__()
        loadUi('ui/accountUI.ui',self)

        self.setWindowTitle("My Account")

        #buttons present on form
        self.editPass.clicked.connect(self.edit_pass)
        self.editWeight.clicked.connect(self.edit_weight)
        self.logoutButton.clicked.connect(self.logout_account)
        self.delAccountB.clicked.connect(self.del_account)
        self.backEButton.clicked.connect(self.exit_dialog)

        self.weight = weight
        self.U_ID = U_ID

        self.user_info()

    #getting userd info to put into qlineedits
    def user_info(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()

            # getting user's information from the database
            query = "SELECT U_Password, U_Weight FROM tblUser WHERE U_ID = %s"
            cursor.execute(query, (self.U_ID,))
            user_info = cursor.fetchone()

            if user_info:
                self.leUName.setText(self.U_ID)
                self.leUName.setReadOnly(True)
                self.lePass.setText(user_info[0])
                self.leUWeight.setText(str(user_info[1])) 

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

    def edit_pass(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            passw = self.lePass.text()

            if not passw:
                QMessageBox.warning(self, "Warning", "Cannot be empty")
                return

            query = "UPDATE tblUser SET U_Password = %s WHERE U_ID = %s"
            cursor.execute(query, (passw, self.U_ID))
            cnx.commit()

            QMessageBox.information(self, "Updated", "Your password has been updated.")

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

    def edit_weight(self):
        try:    
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            weyt = self.leUWeight.text()

            if not weyt:
                QMessageBox.warning(self, "Warning", "Weight cannot be empty")
                return

            query = "UPDATE tblUser SET U_Weight = %s WHERE U_ID = %s"
            cursor.execute(query, (weyt, self.U_ID))
            cnx.commit()

            QMessageBox.information(self, "Updated", "Your weight has been updated.")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the connection")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:   
                print(err)
        finally:
            cursor.close()
            cnx.close()

    def logout_account(self):
        self.close()
        sys.exit(0)

    def del_account(self):
        try:
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()

            reply = QMessageBox.question(self, 'Delete Account', 'Are you sure you want to delete your account?')
            if reply == QMessageBox.StandardButton.Yes:
                cursor = cnx.cursor()

                dj_query = "DELETE FROM User_Journal WHERE U_ID = %s"
                cursor.execute(dj_query, (self.U_ID,))
                cnx.commit()

                de_query = "DELETE FROM tblExercise WHERE U_ID = %s"
                cursor.execute(de_query, (self.U_ID,))
                cnx.commit()

                du_query = "DELETE FROM tblUser WHERE U_ID = %s"
                cursor.execute(du_query, (self.U_ID,))
                cnx.commit()

                QMessageBox.information(self, 'Account Deleted', 'Your account has been successfully deleted.')

                sys.exit()

            else:
                return

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the connection")
                
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            cursor.close()
            cnx.close()

    def exit_dialog(self):
        self.reject()


if __name__ == "__main__":
    app =QApplication(sys.argv)
    dashwindow = DashMenu(result[0])
    dashwindow.show()
    sys.exit(app.exec())

