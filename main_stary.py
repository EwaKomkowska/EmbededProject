import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sqlite3
import sys
import time

con = None          #inicjujemy Nonem żeby móc wywołać wyjątek na tym (mieć pewność, że istnieje zmienna)
reader = SimpleMFRC522()


def openDoor():
    cardID = reader.read()
    cur.execute("SELECT COUNT(*) FROM cards WHERE id = ?", cardID)
    liczba = cur.rowcount
    con.commit()            #nie wiem, czy to tu czy przed przypisaniem na liczbę
    if liczba > 0:
        print("The door was opened!!! Please come in.")
        return True
    print("Something was wrong - you haven't got an access to come in :(")
    return False


def writeIntoDatabase():
    text = input('New data (Please enter your name):')
    print("Now place your tag to write")  # po zbliżeniu karty zostanie ona odczytana

    reader.write(text)
    # teraz trzeba dodać to do bazy danych :o
    '''u nas - czy nie trzeba czasem od razu odczytywać z reader id i textu i to wrzucać do bazy???
    na razie zapisujemy tylko nick i id, ale trzeba jeszcze dodać RTC
    można też executescript i wtedy wszystko wrzucić w jedno polecenie, a nie za każdym razem execute'''

    cardID, text = reader.read()
    today = time.localtime()
    cur.execute("CREATE TABLE cards(id INT, name TEXT, data TEXT)")             #ewentualnie DATE/DATETIME, ale to trzeba odfiltrować
    cur.execute("INSERT INTO cards VALUES(?, ?)", (cardID, text, today))

    con.commit()
    print("Written - now you can open the door")


if __name__ == "__main__":              #inicjalizujemy tworząc bazę
    try:
        con = sqlite3.connect('cardsData.db')
        cur = con.cursor()
        choose = input("1 - Write into database, 2 - open the door, 3 - exit")
        while 1:           #jak to zmienić???
            if int(choose) == 1:
                writeIntoDatabase()
            elif int(choose) == 2:
                openDoor()
            else:
                exit(0)

    except sqlite3.Error as e:
        if con:
            con.rollback()

        print("Error {}:".format(e.args[0]))
        sys.exit(1)

    finally:
        GPIO.cleanup()
        if con:
            con.close()



