import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QWidget, QMainWindow
from PyQt5.uic.properties import QtCore
from PyQt5 import QtCore
import sqlite3

progressBarValue = 0

#ekran powitalny
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.appProgress)
        self.timer.start(30)

#funkcja paska postępu
    def appProgress(self):
        global progressBarValue
        self.progressBar.setValue(progressBarValue)

        if progressBarValue > 25 and progressBarValue < 65:
            self.loadingLabel.setText("Sprawdzanie parametrów zbiornika...")

        elif progressBarValue > 65 and progressBarValue <100:
            self.loadingLabel.setText("Wczytywanie bazy danych...")

        elif progressBarValue == 100:
            self.timer.stop()
            self.gotoMain()
        
        progressBarValue+=1

#przejście do głównej aplikacji
    def gotoMain(self):
        mainapp=MainMenuScreen()
        widget.addWidget(mainapp)
        widget.setCurrentIndex(widget.currentIndex()+1)

#główne aplikacja
class MainMenuScreen(QMainWindow):
    def __init__(self):
        super(MainMenuScreen, self).__init__()
        loadUi("untitled.ui", self)
        self.currentTime = QtCore.QTimer()
        self.currentTime.timeout.connect(self.displayTime)
        self.currentTime.start(0)
        currentDate = QtCore.QDate.currentDate()
        displayDate = currentDate.toString('dd/MM/yyyy')
        self.currentDateLabel.setText(displayDate)
        self.settingsButton.mousePressEvent = self.goToSettingsLoginFromMenu
        self.homeButton.mousePressEvent = self.goToMainMenuFromMenu
        self.homeButton.setEnabled(False)
        self.settingsButton.setEnabled(False)
#początkowy alert
        self.startAlertButton.clicked.connect(self.goToLogin)

#logowanie się do aplikacji
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.loginFunction)

#logowanie się do ustawień
        self.settingsPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.settingsLoginButton.clicked.connect(self.adminLogin)

#przejście do logowania
    def goToLogin(self):
        self.mainApp.setCurrentWidget(self.appLogin)

#funkcja logowania się    
    def loginFunction(self):
        user = self.userNameField.text()
        password = self.passwordField.text()
        self.errorlabel.setText("")

        if len(user)==0 or len(password)==0:
            self.errorlabel.setText("Uzupełnij wszystkie pola")

        else:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            query = 'SELECT password FROM login_info WHERE username =\''+user+"\'"
            cur.execute(query)

            try:
                result_pass = cur.fetchone()[0]
                if result_pass == password:
                    self.goToMainMenu()
                    conn.close()
            except:
                self.errorlabel.setText("Nieprawidłowa nazwa użytkownika lub hasło")

#przejście do głownego menu
    def goToMainMenu(self):
        self.mainApp.setCurrentWidget(self.mainMenu)
        self.settingsButton.setEnabled(True)
        self.homeButton.setEnabled(False)

# przejście do głownego menu z poziomu górnego menu
    def goToMainMenuFromMenu(self, event):
        self.mainApp.setCurrentWidget(self.mainMenu)
        self.settingsButton.setEnabled(True)
        self.homeButton.setEnabled(False)

#przejście do logowanie się do ustawień
    def goToSettingsLogin(self):
        self.mainApp.setCurrentWidget(self.settingsLogin)
        self.homeButton.setEnabled(True)
        self.settingsButton.setEnabled(False)

# przejście do logowanie się do ustawień z poziomu górnego menu
    def goToSettingsLoginFromMenu(self, event):
        self.mainApp.setCurrentWidget(self.settingsLogin)
        self.homeButton.setEnabled(True)
        self.settingsButton.setEnabled(False)

#logowanie się do ustawień
    def adminLogin(self):
        adminpassword = '1234'
        password = self.settingsPassword.text()
        self.settingsErrorLabel.setText("")

        if len(password)==0:
            self.settingsErrorLabel.setText("Uzupełnij wszystkie pola")
        elif password == adminpassword:
            self.goToSettings()
            self.homeButton.setEnabled(True)
        elif password != adminpassword:
            self.settingsErrorLabel.setText("Hasło nieprawidłowe")

#przejście do ustawień
    def goToSettings(self):
        self.mainApp.setCurrentWidget(self.appSettings)
        self.settingsButton.setEnabled(False)

#wyświetlanie aktualnego czasu
    def displayTime(self):
        currentTime = QtCore.QTime.currentTime()
        displayTime = currentTime.toString('hh:mm:ss')
        self.currentTimeLabel.setText(displayTime)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Kriokomora lokalna")
    widget = QStackedWidget()
    welcome = WelcomeScreen()

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

