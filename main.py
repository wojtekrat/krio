import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QMainWindow, QSlider
from PyQt5.uic.properties import QtCore
from PyQt5 import QtCore
import sqlite3
import time

progressBarValue = 0
iloscZabiegow = 0

# ekran powitalny
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.appProgress)
        self.timer.start(30)

    # funkcja paska postępu
    def appProgress(self):
        global progressBarValue
        self.progressBar.setValue(progressBarValue)

        if progressBarValue > 25 and progressBarValue < 65:
            self.loadingLabel.setText("Sprawdzanie parametrów zbiornika...")

        elif progressBarValue > 65 and progressBarValue < 100:
            self.loadingLabel.setText("Wczytywanie bazy danych...")

        elif progressBarValue == 100:
            self.timer.stop()
            self.gotoMain()

        progressBarValue += 1

    # przejście do głównej aplikacji
    def gotoMain(self):
        mainapp = MainMenuScreen()
        widget.addWidget(mainapp)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# główne aplikacja
class MainMenuScreen(QMainWindow):
    def __init__(self):
        super(MainMenuScreen, self).__init__()
        loadUi("untitled.ui", self)

        #laczenie z baza danych
        self.conn = sqlite3.connect("userdata.db")
        self.updateProceduresQuantity(0)

        # aktualny czas
        self.currentTime = QtCore.QTimer()
        self.currentTime.timeout.connect(self.displayTime)
        self.currentTime.start(0)
        self.currentDate = QtCore.QDate.currentDate()
        self.displayDate = self.currentDate.toString('dd/MM/yyyy')
        self.currentDateLabel.setText(self.displayDate)

        # menu glowne gorne
        self.settingsButton.mousePressEvent = self.goToSettingsLoginFromMenu
        self.homeButton.mousePressEvent = self.goToMainMenuFromMenu
        self.infoButton.mousePressEvent = self.goToInfo
        self.homeButton.setEnabled(False)
        self.settingsButton.setEnabled(False)
        self.infoButton.setEnabled(False)

        # początkowy alert
        self.startAlertButton.clicked.connect(self.goToLogin)

        # logowanie się do aplikacji
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.loginFunction)

        # logowanie się do ustawień
        self.settingsPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.settingsLoginButton.clicked.connect(self.adminLogin)

        # przejście do wybranego trybu
        self.autoButton.clicked.connect(self.goToAuto)
        self.manualButton.clicked.connect(self.goToManual)

        #ustawianie czasu zabiegu (minuty)
        self.minutesLabel.mousePressEvent = self.goToSelectTimeMinutes
        self.timeSelectMinutesAcceptButton.clicked.connect(self.goToManual)
        self.selectTimeMinutesSpinBox.setValue(0)
        self.selectTimeMinutesSpinBox.setMinimum(0)
        self.selectTimeMinutesSpinBox.setMaximum(59)
        self.selectTimeMinutesSpinBox.valueChanged.connect(self.setSelectedTimeMinutes)

        #ustawienia czasu zabiegu (sekundy)
        self.secondsLabel.mousePressEvent = self.goToSelectTimeSeconds
        self.timeSelectSecondsAcceptButton.clicked.connect(self.goToManual)
        self.selectTimeSecondsSpinBox.setValue(0)
        self.selectTimeSecondsSpinBox.setMinimum(0)
        self.selectTimeSecondsSpinBox.setMaximum(59)
        self.selectTimeSecondsSpinBox.valueChanged.connect(self.setSelectedTimeSeconds)

        # ustawienie natezenia
        self.intensitySlider.valueChanged.connect(self.updateIntensity)
        self.intensitySlider.setMaximum(100)
        self.intensitySlider.setMinimum(0)
        self.intensitySlider.setTickInterval(10)
        self.intensitySlider.setTickPosition(QSlider.TicksBothSides)
        self.intensitySlider.setValue(10)
        #przycisk rozpoczecia zabiegu
        self.startButton.clicked.connect(self.startProcess)
        #przycisk pokazania wszystkich dotychczasowych zabiegow
        self.allProceduresButton.clicked.connect(self.goToAllProcedures)
        self.tableWidget.setColumnWidth(0, 229)
        self.tableWidget.setColumnWidth(1, 279)

    # przejście do logowania
    def goToLogin(self):
        self.mainApp.setCurrentWidget(self.appLogin)

    # funkcja logowania się
    def loginFunction(self):
        user = self.userNameField.text()
        password = self.passwordField.text()
        self.errorlabel.setText("")

        if len(user) == 0 or len(password) == 0:
            self.errorlabel.setText("Uzupełnij wszystkie pola")

        else:
            
            cur = self.conn.cursor()
            query = 'SELECT password FROM login_info WHERE username =\'' + user + "\'"
            cur.execute(query)

            try:
                result_pass = cur.fetchone()[0]
                if result_pass == password:
                    self.goToMainMenu()
                    cur.close()
            except:
                self.errorlabel.setText("Nieprawidłowa nazwa użytkownika lub hasło")

    # przejście do głownego menu
    def goToMainMenu(self):
        self.mainApp.setCurrentWidget(self.mainMenuSelect)
        self.settingsButton.setEnabled(True)
        self.homeButton.setEnabled(False)
        self.infoButton.setEnabled(True)

    # przejście do głownego menu z poziomu górnego menu
    def goToMainMenuFromMenu(self, event):
        self.mainApp.setCurrentWidget(self.mainMenuSelect)
        self.settingsButton.setEnabled(True)
        self.homeButton.setEnabled(False)
        self.infoButton.setEnabled(True)

    # przejście do logowanie się do ustawień
    def goToSettingsLogin(self):
        self.mainApp.setCurrentWidget(self.settingsLogin)
        self.homeButton.setEnabled(True)
        self.settingsButton.setEnabled(False)
        self.infoButton.setEnabled(True)
        self.settingsPassword.setText("")
        self.settingsErrorLabel.setText("")

    # przejście do logowanie się do ustawień z poziomu górnego menu
    def goToSettingsLoginFromMenu(self, event):
        self.mainApp.setCurrentWidget(self.settingsLogin)
        self.homeButton.setEnabled(True)
        self.settingsButton.setEnabled(False)
        self.infoButton.setEnabled(True)
        self.settingsPassword.setText("")
        self.settingsErrorLabel.setText("")

    # logowanie się do ustawień
    def adminLogin(self):
        adminpassword = '1234'
        password = self.settingsPassword.text()
        self.settingsErrorLabel.setText("")

        if len(password) == 0:
            self.settingsErrorLabel.setText("Uzupełnij wszystkie pola")
        elif password == adminpassword:
            self.goToSettings()
            self.homeButton.setEnabled(True)
        elif password != adminpassword:
            self.settingsErrorLabel.setText("Hasło nieprawidłowe")

    # przejście do ustawień
    def goToSettings(self):
        self.mainApp.setCurrentWidget(self.appSettings)
        self.settingsButton.setEnabled(False)
        self.infoButton.setEnabled(True)


    # wyświetlanie aktualnego czasu
    def displayTime(self):
        currentTime = QtCore.QTime.currentTime()
        displayTime = currentTime.toString('hh:mm:ss')
        self.currentTimeLabel.setText(displayTime)

    # przejście do trybu manualnego
    def goToAuto(self):
        self.mainApp.setCurrentWidget(self.mainMenuAuto)
        self.homeButton.setEnabled(True)

    # przejście do trybu automatycznego
    def goToManual(self):
        self.mainApp.setCurrentWidget(self.mainMenuManual)
        self.homeButton.setEnabled(True)

    #ustawienia czasu zabiegu
    def goToSelectTimeMinutes(self, event):
        self.mainApp.setCurrentWidget(self.selectTimeMinutes)

    def goToSelectTimeSeconds(self, event):
        self.mainApp.setCurrentWidget(self.selectTimeSeconds)

    def setSelectedTimeMinutes(self):
        minutes = str(self.selectTimeMinutesSpinBox.value())
        self.minutesLabel.setText(minutes.zfill(2))

    def setSelectedTimeSeconds(self):
        seconds = str(self.selectTimeSecondsSpinBox.value())
        self.secondsLabel.setText(seconds.zfill(2))

    #odmierzanie czasu
    def timez(self, m, s):
        t = (m * 60) + (s)

        while t > 0 and t != 0:
            while s > 0 or m > 0:
                if s != 0:
                    time.sleep(1)
                    self.minutesLabel.setText(str(m).zfill(2))
                    self.secondsLabel.setText(str(s).zfill(2))
                    QApplication.processEvents()
                    t -= 1
                    s -= 1

                elif m > 0:
                    s = 60
                    m -= 1
            time.sleep(1)
            self.secondsLabel.setText("00")
            self.selectTimeSecondsSpinBox.setValue(0)
            self.selectTimeMinutesSpinBox.setValue(0)
            break

    # aktualizowanie stanu natężenie
    def updateIntensity(self, event):
        self.intensityLabel.setText(str(event))

    def startProcess(self):
        seconds = str(self.selectTimeSecondsSpinBox.value())
        minutes = str(self.selectTimeMinutesSpinBox.value())
        self.timez(int(minutes), int(seconds))
        self.updateProceduresQuantity(1)
        self.updateProceduresList()

    def goToInfo(self, event):
        self.mainApp.setCurrentWidget(self.infoPage)
        self.homeButton.setEnabled(True)
        self.settingsButton.setEnabled(True)
        self.infoButton.setEnabled(False)

    def updateProceduresQuantity(self, x):
        c = self.conn.cursor()
        c.execute('SELECT * FROM ile_zabiegow')
        data = c.fetchone()[0]

        iloscBazowa = data
        ilosc = iloscBazowa + x
        c.execute("""UPDATE ile_zabiegow SET ilosc = :ilosc""", {
            'ilosc': ilosc
        })
        self.conn.commit()
        self.proceduresQuantityLabel.setText(str(ilosc))
        c.close()
    
    def updateProceduresList(self):
        c = self.conn.cursor()
        records = [str(self.userNameField.text()), ((self.displayDate) + ' ' + str(self.currentTimeLabel.text()))]
        c.execute("INSERT INTO wszystkie_zabiegi VALUES (?,?) ;", records)
        self.conn.commit()
        c.close()

    def goToAllProcedures(self):
        self.mainApp.setCurrentWidget(self.allProcedures)
        self.updateTable()

    def updateTable(self):
        c = self.conn.cursor()
        query = "SELECT * FROM wszystkie_zabiegi"
        c.execute(query)
        data = c.fetchall()

        self.tableWidget.setRowCount(len(data))
        tablerow = 0
        for row in data:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            tablerow += 1
        c.close()

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
