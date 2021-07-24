import mysql.connector
import random


def main():
    db = Puntos()
    cursor = db.cursor()
    tienda = generar_tienda(cursor)
    print()
    bunko = generar_bunko(cursor)

    f = open(".yast/tienda.yast", "w", encoding="utf-8")
    for x in tienda:
        f.write(x)
        f.write("\n")
    f.close()

    f = open(".yast/bunko.yast", "w", encoding="utf-8")
    for x in bunko:
        f.write(x)
        f.write("\n")
    f.close()

def Puntos():
    db = mysql.connector.connect(
        host="localhost",
        user="Arth",
        password="YastBots4",
        database="yastabot"
    )
    return db


def generar_tienda(cursor):
    result_text = []
    tienda = []
    cursor.execute("SELECT * FROM items_tienda")
    result = cursor.fetchall()

    for x in result:
        result_text.append(str(x[0]).split(","))

    for x in range(0, len(result_text)):
        result_text[x] = str(result_text[x]).split("'")[1]

    for x in range(0, 3):
        item = result_text[random.randint(0, len(result_text) - 1)]
        if item not in tienda:
            tienda.append(item)
        else:
            while item in tienda:
                item = result_text[random.randint(0, len(result_text) - 1)]
            tienda.append(item)

    print("Items tienda:")
    for x in tienda:
        print(x)
    return tienda


def generar_bunko(cursor):
    bunko = []
    cursor.execute("SELECT * FROM items_bunko")
    result = cursor.fetchall()
    result_text = []

    for x in result:
        if "PhoneWave?" in x:
            x = ("PhoneWave™", 0)
        result_text.append(str(x[0]).split(","))

    for x in range(0, len(result_text)):
        result_text[x] = str(result_text[x]).split("'")[1]

    for x in range(0, 3):
        item = result_text[random.randint(0, len(result_text) - 1)]
        if item not in bunko:
            bunko.append(item)
        else:
            while item in bunko:
                item = result_text[random.randint(0, len(result_text) - 1)]
            bunko.append(item)

    print("Items bunko:")

    for x in bunko:
        print(x)
    return bunko
