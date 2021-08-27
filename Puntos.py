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
    precios = []
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
    for x in range(0, 3):
        cursor.execute(f"SELECT cost FROM items WHERE item_name='{tienda[x]}'")
        result = cursor.fetchall()
        precios.append(str(result[0]).split(",")[0].split("(")[1])
    for x in range(0, len(tienda)):
        tienda[x] = tienda[x] + ": " + precios[x]
    print("Items tienda: ")
    for x in tienda:
        print(x)
    return tienda


def generar_bunko(cursor):
    bunko = []
    precios = []
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

    for x in range(0, 3):
        item = bunko[x]
        if item == "PhoneWave™":
            item = "PhoneWave?"
        cursor.execute(f"SELECT cost FROM items WHERE item_name='{item}'")
        result = cursor.fetchall()
        precios.append(str(result).split(",")[0].split("(")[1])

    for x in range(0, len(bunko)):
        bunko[x] = bunko[x] + ": " + precios[x]
    print("Items bunko:")
    for x in bunko:
        print(x)
    return bunko


def comprobar(user):
    db = Puntos()
    cursor = db.cursor()
    cursor.execute(f"SELECT points FROM users WHERE username='{user}'")
    result = cursor.fetchall()
    if len(result) == 0:
        return -1
    else:
        pts = int(str(result[0]).split(",")[0].split("(")[1])
        cursor.execute(f"SELECT name FROM users WHERE username='{user}'")
        result = cursor.fetchall()
        name = str(result[0]).split(",")[0].split("(")[1].split("'")[1]
        if name == "NULL" and pts == 0:
            return -1
        else:
            return pts


def registrar(user, name):
    db = Puntos()
    cursor = db.cursor()
    cursor.execute(f"SELECT username FROM users WHERE username='{user}'")
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.callproc('registrar', (f"{user}", f"{name}"))
    else:
        cursor.callproc('actualizar', (f"{user}", f"{name}"))
    db.commit()
    print(str(result))


def perfil_propio(user):
    user = str(user)
    db = Puntos()
    cursor = db.cursor()
    cursor.execute(f"SELECT name, points FROM users WHERE username='{user}'")
    result = cursor.fetchall()
    if len(result) != 0:
        perfil = str(result).split("(")[1].split(")")[0].split(", ")
        perfil[0] = perfil[0].split("'")[1]
        perfil[1] = int(perfil[1])
    else:
        perfil = None
    return perfil


def perfil_ajeno(user):
    user = str(user)
    db = Puntos()
    cursor = db.cursor()
    cursor.execute(f"SELECT name, points FROM users WHERE username='{user}'")
    result = cursor.fetchall()
    if len(result) != 0:
        perfil = str(result).split("(")[1].split(")")[0].split(", ")
        perfil[0] = perfil[0].split("'")[1]
        perfil[1] = int(perfil[1])
    else:
        perfil = None
    return perfil


def equipo(user):
    user = str(user)
    db = Puntos()
    cursor = db.cursor()
    cursor.execute(f"SELECT item FROM inventarios WHERE username='{user}' AND slot > 12")
    result = cursor.fetchall()
    if len(result) == 0:
        lista = None
    else:
        arma = str(result[0]).split("'")[1]
        armadura = str(result[1]).split("'")[1]
        lista = f"Tu arma es el {arma} y tu armadura la {armadura}"
    return lista


def equipo_ajeno(user):
    db = Puntos()
    cursor = db.cursor()
    cursor.execute(f"SELECT item FROM inventarios WHERE username='{user}' AND slot > 12")
    result = cursor.fetchall()
    if len(result) == 0:
        lista = None
    else:
        arma = str(result[0]).split("'")[1]
        armadura = str(result[1]).split("'")[1]
        lista = f"Su arma es el {arma} y su armadura la {armadura}"
    return lista


def inventario(user):
    db = Puntos()
    cursor = db.cursor()
    cursor.execute(f"SELECT item FROM inventarios WHERE slot<10 AND username='{user}'")
    result = cursor.fetchall()
    if len(result) == 0:
        lista = None
    else:
        for x in range(0, len(result)):
            result[x] = str(result[x]).split("'")[1]
        print(result)
        lista = ""
        for x in result:
            if len(lista) == 0:
                lista = x
            else:
                lista = lista + ", " + x
        print(lista)
    return lista


def tienda():
    archivo_tienda = open(".yast/tienda.yast", "r", encoding="utf-8")
    items = archivo_tienda.readlines()
    print(items)
    lista = ""
    for x in range(0, len(items)):
        if x == 2:
            lista = lista + items[x].split('\n')[0]
        else:
            lista = lista + items[x].split('\n')[0] + ", "
    archivo_tienda.close()
    return lista


def bunko():
    archivo_bunko = open(".yast/bunko.yast", "r", encoding="utf-8")
    items = archivo_bunko.readlines()
    lista = ""
    for x in range(0, len(items)):
        if x == 2:
            lista = lista + items[x].split('\n')[0]
        else:
            lista = lista + items[x].split('\n')[0] + ", "
    archivo_bunko.close()
    return lista
