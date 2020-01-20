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

'''reader = SimpleMFRC522()'''
'''ds3231 = SDL_DS3231.SDL_DS3231(1, 0x68)'''


def baza():
    cur.execute("create table if not exists Cards(id INT, name TEXT, data TEXT)")
    cur2.execute("create table if not exists Logs(id INT)")

    try:
        cur.execute("insert into Cards values(1, 'nazwa', 'data')")
        cur.execute("insert into Cards values(2, 'nazwa2', 'data2')")
        cur.execute("insert into Cards values(3, 'nazwa3', 'data3')")
        #cur.execute("delete from Cards where id = 1")
        cur2.execute("insert into Logs values(1)")
        #cur2.execute("delete from Logs where id = 1")

    except sqlite3.Error as e:
        print("Error {}:".format(e.args[0]))


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

        self.tableList = QTableWidget(self)
        self.tableList.setRowCount(0)

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

        '''self.pybutton = QPushButton('OK', self)
        self.pybutton.clicked.connect(self.clickMethod)
        self.pybutton.move(80, 60)'''

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def recurring_timer(self):
        self.counter += 1
        self.label.setText("Counter: %d" % self.counter)

    def init_TableList(self):
        cur.execute('''SELECT * FROM Cards ''')
        rows = cur.fetchall()
        print("Len rows: ", len(rows))

        self.tableList.setEnabled(False)            #wygląda śrendnio, ale działa
        self.tableList.setRowCount(len(rows))
        self.tableList.setColumnCount(3)
        self.tableList.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableList.setHorizontalHeaderLabels(["UserName", "CardID", "Data"])

        self.tableList.setRowCount(0)
        counter = 0
        for row in rows:
            self.tableList.insertRow(counter)
            self.tableList.setItem(counter, 0, QTableWidgetItem(str(row[0])))
            self.tableList.setItem(counter, 1, QTableWidgetItem(row[1]))
            self.tableList.setItem(counter, 2, QTableWidgetItem(row[2]))
            counter += 1
            print(counter)

        #cardsRows = [[1, "Id 0", "data 0"], [2, "Id 1", "data 1"]]

    def keyPressEvent(self, event):
        # dodać obsługę bazy
        try:
            if event.key() == Qt.Key_1:
                writeIntoDatabase()
                print("Zapisanie do bazy")
            elif event.key() == Qt.Key_2:
                openDoor()
                print("A teraz drzwi")
            elif event.key() == Qt.Key_3:
                exit(0)
                print("Wychodzimy")
            elif event.key() == Qt.Key_4:
                cur.execute("drop table Cards")
                print("Czyszczenie bazy")
            elif event.key() == Qt.Key_5:
                self.init_TableList()
                print("wyswietlam wszystkie")
            else:
                print('Wrong output')

        except sqlite3.Error as e:
            if con:
                con.rollback()

            print("Error {}:".format(e.args[0]))
            exit(0)

        '''finally:
            GPIO.cleanup()
            if con:
                con.close()'''

        # odczyt karty - tutaj ma byc po prostu dodanie do bazy logów?
        # cardID, text = 1, "text" '''= reader.read()'''
        # wyświetlenie nowego przedmiotu w tabeli - trzeba stworzyć dodakową bazę na logi
        #

    def clickMethod(self):
        time.sleep(5)

    def initGrid(self):
        self.init_TableList()

        cur.execute("select * from Cards")
        rowDatabase = cur.fetchall()  # 2
        print(rowDatabase)
        print("Len: ", len(rowDatabase))

        logsDatabaseRow = cur2.fetchall()   #5
        logsRows = []        #= ["Log1", "Log2", "Log3", "Log4", "Log5"]
        for elem in logsDatabaseRow:
            logsRows.append(elem)

        self.logs = QTableWidget(self)
        #self.logs.setEditTriggers(QAbstractItemView.SelectedClicked)         #ż☺eby nie móc edytować tabeli
        self.logs.setEnabled(False)
        self.logs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.logs.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # rozciąganie kolumn
        self.logs.setRowCount(len(logsDatabaseRow))

        self.logs.setColumnCount(1)
        self.logs.setHorizontalHeaderLabels(["Logs(CardID)"])

        # tutaj odczytujemy dane z bazy
        for i in range(len(logsDatabaseRow)):
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
    con = sqlite3.connect('cardsData.db')
    con2 = sqlite3.connect('logsData.db')
    cur = con.cursor()
    cur2 = con2.cursor()

    while 1:
        ex = MainWindow()
        ex.show()
        sys.exit(app.exec_())
