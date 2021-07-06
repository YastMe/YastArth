import random

from pygame import mixer
import Sender
import time
import Parser


def main():
    chat = open("chat.txt", "r", encoding="utf-8")
    users = []
    x = 1

    cd = [0, 0, 18000, 0, 0]  ##Lista de cooldowns.
    # Cooldown = segundos * 10
    # 0 = Gift
    # 1 = Bunko
    # 2 = Anuncios
    # 3 = Participantes locke
    # 4 = NullPo

    while True:
        print(x)
        lineas = chat.readlines()
        lineas_prev = len(lineas)
        Parser.parse()
        chat.seek(0)
        lineas = chat.readlines()
        lineas_act = len(lineas)
        print(f"Ahora: {lineas_act}, Antes: {lineas_prev}")
        comprobar(lineas, lineas_act, lineas_prev, cd, users)
        chat.seek(0)
        time.sleep(0.1)
        x += 1
        for i in range(0, len(cd)):
            if cd[i] > 0:
                cd[i] -= 1
        if cd[2] == 0:
            cd = ad(cd)
        if x == 2500:
            x = 0
            chat.close()
            chat = open("chat.txt", "r", encoding="utf-8")


def comprobar(lineas, lineas_act, lineas_prev, cd, users):  ##Comprobación y ejecución de comandos
    if lineas_act > lineas_prev:
        msg = lineas[lineas_act - 1].split("', '")[1].split("'")[0]
        usr = lineas[lineas_act - 1].split("', '")[0].split("'")[1]
        if usr not in users and usr != "yastarth":
            users.append(usr)
            saludar(usr)
        if len(msg) > 0:
            if msg[0] == '!':
                cmd(msg, usr, cd)
            if msg.lower() == "nullpo" or msg.lower() == "nullpointerexception":
                if cd[4] == 0:
                    gah(usr)
                    cd[4] = 3000
                else:
                    cooldown_failed(usr, "nullpo", cd[4])


def cmd(msg, user, cd):
    command = msg.split("!")[1].split(" ")[0]
    if len(msg.split(" ")) > 1:  ##Comandos apuntados
        dest = msg.split("!")[1].split(" ")[1]
        if command == "gift":  ##!gift
            if cd[0] == 0:
                gift(user, dest)
                cd[0] = 1200
            else:
                cooldown_failed(user, command, cd[0])

    else:  ##Comandos simples
        if command == "bunko":  ##!bunko
            if cd[1] == 0:
                bunko(user)
                cd[1] = 50
            else:
                cooldown_failed(user, command, cd[1])
        if command == "comandos":
            lista(user)
        if command == "participantes":
            participantes(user)
        if command == "normas":
            normas(user)

    return cd


def cooldown_failed(user, cmds, cd):
    if cd < 60:
        Sender.chat(
            f"/me {user}, por favor, espera un poco antes de usar el comando {cmds}. ¡Solo falta(n) {int(cd / 10)}"
            f" segundo(s)!")
    else:
        mins = int(cd / 10 / 60)
        secs = int(cd / 10)
        for i in range(0, mins):
            secs = secs - 60
        round(secs)
        if mins < 2:
            Sender.chat(f"/me {user}, por favor, espera un poco antes de usar el comando {cmds}. ¡Solo falta {mins}"
                        f" minuto y {secs} segundo(s)!")
        else:
            Sender.chat(f"/me {user}, por favor, espera un poco antes de usar el comando {cmds}. ¡Solo faltan {mins}"
                        f" minutos y {secs} segundo(s)!")


def gift(user, dest):
    mixer.init()
    sonido = mixer.Sound("Sonidos/gift.mp3")
    Sender.chat(f"/timeout {dest} 60 Gift")
    Sender.chat(f"/me ¡{user} ha envenenado a {dest}! Y no me queda maná para curarle...")
    sonido.play()


def bunko(user):
    mixer.init()
    sonido = mixer.Sound("Sonidos/EL_BUNKO.mp3")
    Sender.chat(f"/me ¡{user}, que no es un búnker, deja de llamarlo así!")
    sonido.play()


def lista(user):
    Sender.chat(f"/me {user}, la lista de comandos es la siguiente:")
    Sender.chat(
        "/me Comandos simples (no necesitas especificar a quién los apuntas): !bunko, !normas y !participantes. "
        "Y por lo que más queráis, dejad de decir nullpo")
    Sender.chat("/me Comandos apuntados (debes especificar a quién los diriges): !gift")


def saludar(user):
    Sender.chat(f"/me ¡Hola, {user}!")


def ad(cd):
    Sender.chat("/commercial 60")
    cd[2] = 18000
    return cd


def participantes(user):
    Sender.chat(
        f"/me {user}, los participantes son los siguientes: Zetaeme_youtube, VSharkness, comandante_shepard, arocet,"
        f" anuhiu, streamfran, streampatt, hatosito, moonxwisher, kiarafey, niacosplay, mikuchinatsu,"
        f" pipono_laura, zigredyt, matycyndapoke y YastMe")


def normas(user):
    Sender.chat(f"/me {user}, las normas están en el siguiente enlace: https://pastebin.com/c9R2qPaB")


def gah(user):
    mixer.init()
    Sender.chat("Gah!")
    sonido = mixer.Sound("Sonidos/gah.mp3")
    sonido.play()
    time.sleep(60)
    Sender.chat(f"/me ¡{user}, no hagas eso!")
    sonido = mixer.Sound("Sonidos/bonk.mp3")
    sonido.play()
    if random.randint(1, 20) == 20:
        Sender.chat(f"/timeout {user} 10 Bonk")
