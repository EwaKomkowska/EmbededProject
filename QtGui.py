from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time
import sqlite3
'''import SDL_DS3231 ## RTC'''

#dtoverlay=i2c-rtc,ds1307
#nano /boot/config.txt
#dtoverlay=i2c-rtc,ds3231

#sudo i2cdetect -y 1

con = sqlite3.connect('cardsData.db')
'''reader = SimpleMFRC522()'''
'''ds3231 = SDL_DS3231.SDL_DS3231(1, 0x68)'''


def baza():
    global cur
    cur = con.cursor()
    cur.execute("create table if not exists Cards(id INT, name TEXT, data TEXT)")

    try:
        cur.execute("insert into Cards values(1, 'nazwa', 'data')")
        cur.execute("delete from Cards where id = 1")
    except Exception:
        print("Error {}:".format(Exception.args[0]))


def openDoor():
    cardID, text = 1, "text" '''= reader.read()'''

    cur.execute("select * from Cards where id = ?, (cardID, )")

    rows = cur.fetchall()
    for r in rows:
        print(r)

    number = len(rows)
    con.commit()
    if number > 0:
        print("Welcome to the sky, Mr/Mrs")
        return True


def writeIntoDatabase():
    # check if already exists
    # if exists:
    #   print(error)
    # else:
    # write()

    text = input('New data (please enter your name):')
    print('Now place your tag to write')

    '''reader.write(text)'''
    cardID, text = 1, "text" '''reader.read()'''
    print(text)

    #today = time.localtime()
    today = 'dzisiaj'

    print('cardID = ', cardID)
    print('text = ', text)
    print('today = ', today)

    cur.execute("insert into Cards values(?, ?, ?)", (cardID, text, today))
    con.commit()
    print('Written')


class MainWindow(QWidget):
    def __init__(self):
        QMainWindow.__init__(self)

        app.setStyle('Fusion')
        self.window = QWidget(self)
        self.window.setWindowTitle("System to open the door")
        self.window.setGeometry(50, 50, 500, 300)

        self.label = QLabel(self)
        self.label.setText("Instrukcja obsługi:\n1 - wyświetl całą bazę\n2 - wyczyść bazę")
        self.label.setStyleSheet(" font-size: 15px; font-family: Courier New;")  # qproperty-alignment: AlignJustify;
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.info = QLabel(self)
        self.info.setText("Tu jest label do wyświetlania wyniku procedury")
        self.info.setStyleSheet(" font-size: 15px; font-family: Courier New; qproperty-alignment: AlignRight")
        self.info.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.initGrid()
        self.setGrid()
        self.counter = 0

        #podłączenie do bazy
        baza()

        self.pybutton = QPushButton('OK', self)
        self.pybutton.clicked.connect(self.clickMethod)
        self.pybutton.move(80, 60)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def recurring_timer(self):
        self.counter += 1
        self.label.setText("Counter: %d" % self.counter)

        # dodać obsługę bazy
        #try:
        choose = input("1 - Write, 2 - Open, 3 - exit, 4 - drop, 5 - select all\n")
        '''if int(choose) == 1:
                    writeIntoDatabase()
                if int(choose) == 2:
                    openDoor()
                    app.event(None)
                if int(choose) == 3:
                    exit(0)
                if int(choose) == 4:
                    cur.execute("drop table Cards")
                if int(choose) == 5:
                    cur.execute("select * from Cards")
                    rows = cur.fetchall()
                    for r in rows:
                        print(r)
                else:'''
        print('Wrong output')

        '''except sqlite3.Error as e:
            if con:
                con.rollback()

            print("Error {}:".format(e.args[0]))
            exit(0)

        finally:
            GPIO.cleanup()'''
        ''' if con:
                con.close()'''

        # odczyt karty
        # wyświetlenie nowego przedmiotu w tabeli
        #

    def clickMethod(self):
        '''
        if not self.label.text().isdigit():
            self.label.setText('nothing')
            self.tableList.setItem(5, 0, QTableWidgetItem("Useruser"))
            self.tableList.setItem(5, 1, QTableWidgetItem("id id id"))
        else:
            self.label.setText('Pomarańczeee')
        '''
        time.sleep(5)

    def initGrid(self):
        rowDatabase = 2
        cardsRows = [["User0", "Id 0"], ["User1", "Id 1"]]

        self.tableList = QTableWidget(self)
        self.tableList.setRowCount(rowDatabase)
        self.tableList.setColumnCount(2)
        self.tableList.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableList.setHorizontalHeaderLabels(["UserName", "CardID"])

        for i in range(rowDatabase):
            self.tableList.setItem(i, 0, QTableWidgetItem(cardsRows[i][0]))
            self.tableList.setItem(i, 1, QTableWidgetItem(cardsRows[i][1]))

        logsDatabaseRow = 5
        logsRows = ["Log1", "Log2", "Log3", "Log4", "Log5"]

        self.logs = QTableWidget(self)
        self.logs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.logs.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # rozciąganie kolumn
        self.logs.setRowCount(logsDatabaseRow)

        self.logs.setColumnCount(1)
        self.logs.setHorizontalHeaderLabels(["Logs(CardID)"])

        # tutaj odczytujemy dane z bazy
        for i in range(logsDatabaseRow):
            self.logs.setItem(i, 0, QTableWidgetItem(logsRows[i]))

    def setGrid(self):
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.info, 0, 1)
        self.layout.addWidget(self.tableList, 1, 0)
        self.layout.addWidget(self.logs, 1, 1)

        self.setLayout(self.layout)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    while 1:
        ex = MainWindow()
        ex.show()
        sys.exit(app.exec_())
