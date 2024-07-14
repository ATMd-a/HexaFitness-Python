import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
import mysql.connector
from mysql.connector import errorcode
from Users_Journal import DashMenu


#starter
class LogIn (QDialog):
    def __init__(self):
        super().__init__()
        loadUi('ui/LoginUI.ui', self)

        pixmap = QPixmap('others/login_bg.png')
        self.label_3.setPixmap(pixmap)
        
        self.setWindowTitle("HexaFitness App")
        self.loginButton.clicked.connect(self.loginClicked)
        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)

        self.signupDButton.clicked.connect(self.sigup)

    def loginClicked (self):
        userID = self.lineEdit.text()
        password = self.lineEdit_2.text()

        try:
            connection = mysql.connector.connect (host="localhost", user="root", password="Silver.pass1", database="calories")
            cursor = connection.cursor()

            query = "SELECT U_ID, U_Password FROM tblUser WHERE U_ID = %s and U_Password = %s"
            cursor.execute(query, (userID, password))
            result = cursor.fetchone()
        
            if result:
                self.accept()
                self.dash_window = DashMenu(result[0])
                self.dash_window.show()
            else: 
                QMessageBox.warning(self, "Login Failed", "Invalid User name or Password")
                
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Wrong with Username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:   
                print(err)


    def sigup(self):
        pdialog = SignUp()
        pdialog.move(745,195)
        pdialog.exec()

#with no accounts
class SignUp(QDialog):
    connectconfig = {'user':'root', 'password':'Silver.pass1', 'host':'localhost', 'database':'calories'}

    def __init__(self):
        super(SignUp,self).__init__()
        loadUi('ui/SignupUI.ui',self)

        self.setWindowTitle("SignUp")

        self.signupButton.clicked.connect(self.signupClicked)

    def signupClicked (self):
        try:
            #Connect to MySQL
            cnx = mysql.connector.connect(**self.connectconfig)
            cursor = cnx.cursor()
            userID = self.lineEdit.text()
            password = self.lineEdit_2.text()
            weight = self.lineEdit_3.text()
            

            if not userID or not password or not weight:
                QMessageBox.warning(self, "Warning", "Fields cannot be empty.")
                return

            query = "SELECT U_ID FROM tblUser WHERE U_ID = %s"
            cursor.execute(query, (userID,))
            result = cursor.fetchone()
        
            if result:
                QMessageBox.warning(self, "Sign up Failed", "Username already exist.")
                return
                
            query = "INSERT INTO tblUser (U_ID, U_Password, U_Weight) VALUES (%s, %s, %s)"
            cursor.execute(query, (userID, password, weight))
            cnx.commit()

            QMessageBox.information(self, "Sign up Succesful", "Your account has been created.")

            self.close()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Wrong with Username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:   
                print(err)
        else:
            cursor.close()
            cnx.close()

    
if __name__ == "__main__":
    app =QApplication(sys.argv)
    app.setStyleSheet("QWidget { color: black; }")
    loginwindow = LogIn()   
    if loginwindow.exec() == QDialog.accepted:
        print("Login Successful")
    sys.exit(app.exec())

