import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QWidget
from PyQt5.uic.properties import QtCore
from PyQt5 import QtCore
import sqlite3

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.pushButton.clicked.connect(self.gotoAlert)

    def gotoAlert(self):
        alert=AlertScreen()
        widget.addWidget(alert)
        widget.setCurrentIndex(widget.currentIndex()+1)

class AlertScreen(QDialog):
    def __init__(self):
        super(AlertScreen, self).__init__()
        loadUi("alert.ui", self)
        self.pushButton.clicked.connect(self.gotoLogin)

    def gotoLogin(self):
        login=LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.usernamefield.text()
        password = self.passwordfield.text()
        self.errorlabel.setText("")


        if len(user)==0 or len(password)==0:
            self.errorlabel.setText("Uzupełnij wszystkie pola")

        else:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            query = 'SELECT password FROM login_info WHERE username =\''+user+"\'"
            cur.execute(query)
            result_pass = cur.fetchone()[0]
            if result_pass == password:
                print("Zalogowano")
            else:
                self.errorlabel.setText("Nieprawidłowa nazwa użytkownika lub hasło")

app = QApplication(sys.argv)
widget = QStackedWidget()
welcome=WelcomeScreen()


widget.addWidget(welcome)




flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
widget.setWindowFlags(flags)

widget.setFixedHeight(480)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec())
except:
    print("Exiting")