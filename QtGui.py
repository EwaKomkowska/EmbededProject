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

    try:
        cur.execute("insert into Cards values(1, 'nazwa', 'data')")
        cur.execute("delete from Cards where id = 1")

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
    return False


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
    now = time.localtime()
    today = time.strftime("%H:%M:%S", now)

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
        self.label.setText("Instruction: \n1 - Write\n2 - Open the door\n3 - exit\n4 - drop\n5 - select all")
        self.label.setStyleSheet(" font-size: 15px; font-family: Courier New;")  # qproperty-alignment: AlignJustify;
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.info = QLabel(self)
        self.info.setText("Nothing")
        self.info.setStyleSheet(" font-size: 15px; font-family: Courier New; qproperty-alignment: AlignRight")
        self.info.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.initGrid()
        self.setGrid()
        self.counter = 0

        #podłączenie do bazy
        baza()

    def init_TableList(self):
        cur.execute('''SELECT * FROM Cards ''')
        rows = cur.fetchall()

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

    def keyPressEvent(self, event):
        try:
            if event.key() == Qt.Key_1:
                writeIntoDatabase()
                self.info.setText("New data in database")
                self.timer = QTimer(self)
                self.timer.setInterval(10000)
                self.timer.timeout.connect(self.changeLabel)
                self.timer.start()
                print("Zapisanie do bazy")

            elif event.key() == Qt.Key_2:
                #openDoor()
                self.info.setText("The door is open")
                self.timer = QTimer(self)
                self.timer.setInterval(10000)
                self.timer.timeout.connect(self.changeLabel)
                self.timer.start()
                print("A teraz drzwi")

            elif event.key() == Qt.Key_3:
                '''GPIO.cleanup()'''
                self.info.setText("Goodbye")
                if con:
                    con.close()
                print("Wychodzimy")
                exit(0)

            elif event.key() == Qt.Key_4:
                cur.execute("drop table Cards")
                self.info.setText("Nothing in database")
                self.timer = QTimer(self)
                self.timer.setInterval(10000)
                self.timer.timeout.connect(self.changeLabel)
                self.timer.start()
                print("Czyszczenie bazy")
                baza()      #zeby po wyczyszczeniu istniala dalej tablica

            elif event.key() == Qt.Key_5:
                self.init_TableList()
                self.info.setText("You see all data")
                self.timer = QTimer(self)
                self.timer.setInterval(10000)
                self.timer.timeout.connect(self.changeLabel)
                self.timer.start()
                print("wyswietlam wszystkie")

            else:
                print('Wrong output')

        except sqlite3.Error as e:
            if con:
                con.rollback()

            print("Error {}:".format(e.args[0]))
            exit(0)

    def initGrid(self):
        self.init_TableList()

    def changeLabel(self):
        self.info.setText("Nothing")

    def setGrid(self):
        self.layout = QVBoxLayout(self)
        self.layout2 = QHBoxLayout(self)
        self.layout2.addWidget(self.label)
        self.layout2.addWidget(self.info)
        self.layout.addLayout(self.layout2)
        self.layout.addWidget(self.tableList)
        self.setLayout(self.layout)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    con = sqlite3.connect('cardsData.db')
    cur = con.cursor()

    while 1:
        ex = MainWindow()
        ex.show()
        sys.exit(app.exec_())
