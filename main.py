import sqlite3 ## DataBase
'''import SDL_DS3231 ## RTC'''
from PyQt5.QtWidgets import *
import sys

#dtoverlay=i2c-rtc,ds1307
#nano /boot/config.txt
#dtoverlay=i2c-rtc,ds3231

#sudo i2cdetect -y 1

con = sqlite3.connect('cardsData.db')
'''reader = SimpleMFRC522()'''
'''ds3231 = SDL_DS3231.SDL_DS3231(1, 0x68)'''

def init():
    global cur
    cur = con.cursor()
    cur.execute("create table if not exists Cards(id INT, name TEXT, data TEXT)")

    try:
        cur.execute("insert into Cards values(1, 'nazwa', 'data')")
        cur.execute("delete from Cards where id = 1")
    except e:
        print("Error {}:".format(e.args[0]))


def initWindow():
    window.update()

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




if __name__ == "__main__":
    try:
        init()

        app = QApplication(sys.argv)
        app.setStyle('Fusion')

        window = QWidget()
        window.setWindowTitle("System to open the door")
        window.setGeometry(50, 50, 500, 300)  # to zmienić na procent od wyświetlacza

        label = QLabel()
        label.setText("Instruction: 1 - Write\n2 - Open\n3 - exit\n4 - drop\n5 - select all")
        label.setStyleSheet(" font-size: 15px; font-family: Courier New;")  # qproperty-alignment: AlignJustify;
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        info = QLabel()
        info.setText("Tu jest label do wyświetlania wyniku procedury")
        info.setStyleSheet(" font-size: 15px; font-family: Courier New; qproperty-alignment: AlignRight")
        info.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        rowDatabase = 2
        cardsRows = [["User0", "Id 0"], ["User1", "Id 1"]]

        tableList = QTableWidget()
        tableList.setRowCount(rowDatabase)
        tableList.setColumnCount(2)
        tableList.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tableList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        tableList.setHorizontalHeaderLabels(["UserName", "CardID"])

        # pobieranie danych z bazy
        for i in range(rowDatabase):
            tableList.setItem(i, 0, QTableWidgetItem(
                cardsRows[i][0]))  # tu jeszcze trzeba rozlozyc na dwa osobne - nazwa i id
            tableList.setItem(i, 1, QTableWidgetItem(cardsRows[i][1]))

        logsDatabaseRow = 5
        logsRows = ["Log1", "Log2", "Log3", "Log4", "Log5"]

        logs = QTableWidget()
        logs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        logs.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # rozciąganie kolumn
        logs.setRowCount(logsDatabaseRow)

        logs.setColumnCount(1)
        logs.setHorizontalHeaderLabels(["Logs(CardID)"])

        # tutaj odczytujemy dane z bazy
        for i in range(logsDatabaseRow):
            logs.setItem(i, 0, QTableWidgetItem(logsRows[i]))

        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(info, 0, 1)
        layout.addWidget(tableList, 1, 0)
        layout.addWidget(logs, 1, 1)
        window.setLayout(layout)

        window.show()
        # sys.exit(app.exec_())
        app.exec_()

        while 1:
            choose = input("1 - Write, 2 - Open, 3 - exit, 4 - drop, 5 - select all\n")
            initWindow()

            if int(choose) == 1:
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
            else:
                print('Wrong output')

    except sqlite3.Error as e:
        if con:
            con.rollback()

        print("Error {}:".format(e.args[0]))
        exit(0)

    finally:
        '''GPIO.cleanup()'''
        if con:
            con.close()