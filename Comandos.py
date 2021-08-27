import random

from pygame import mixer

import Puntos
import Sender
import time
import Parser


def main():
    chat = open("logs/chat.txt", "r", encoding="utf-8")
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
        try:
            comprobar(lineas, lineas_act, lineas_prev, cd, users)
        except IndexError:
            Sender.chat("/me Lo siento, algo no ha funcionado.")
        chat.seek(0)
        time.sleep(0.1)
        x += 1
        for i in range(0, len(cd)):
            if cd[i] > 0:
                cd[i] -= 1
        if cd[2] == 0:
            cd = ad(cd)


def comprobar(lineas, lineas_act, lineas_prev, cd, users):  ##Comprobación y ejecución de comandos
    if lineas_act > lineas_prev:
        if len(lineas[lineas_act - 1].split(" — ")[0].split("'")) > 0:
            usr = lineas[lineas_act - 1].split(" — ")[0]
            msg = lineas[lineas_act - 1].split(" — ")[1].split('\n')[0]
            if usr not in users and usr != "yastarth":
                users.append(usr)
                saludar(usr)
            if len(msg) > 0:
                if msg.startswith("!"):
                    cmd(msg, usr, cd)
                if msg.lower() == "nullpo" or msg.lower() == "nullpointerexception":
                    if cd[4] == 0:
                        gah(usr)
                        cd[4] = 3000
                    else:
                        cooldown_failed(usr, "nullpo", cd[4])
                if (usr == "renzoxrock" or usr == "ginebra08") and msg.split(" ")[0].lower() == "puto":
                    Sender.chat(f"/me ¡Oye, {usr}! ¡Así no se saluda!")


def cmd(msg, user, cd):
    command = msg.split("!")[1].split(" ")[0]
    if len(msg.split(" ")) > 1 and "puntos" not in msg:  ##Comandos apuntados
        dest = msg.split("!")[1].split(" ")[1]
        if command == "gift":  ##!gift
            if cd[0] == 0:
                gift(user, dest)
                cd[0] = 1200
            else:
                cooldown_failed(user, command, cd[0])

    if "!puntos" in msg:  ##Comandos del sistema de puntos
        puntos(msg, user)
    else:  ##Comandos simples
        if command == "bunko":  ##!bunko
            if cd[1] == 0:
                bunko(user)
                cd[1] = 50
            else:
                cooldown_failed(user, command, cd[1])
        if command == "comandos":
            lista(user)

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
        "/me Comandos simples (no necesitas especificar a quién los apuntas): !bunko, !normas, !participantes y "
        "!equipo. Y por lo que más queráis, dejad de decir nullpo")
    Sender.chat("/me Comandos apuntados (debes especificar a quién los diriges): !gift")


def saludar(user):
    Sender.chat(f"/me ¡Hola, {user}!")


def ad(cd):
    Sender.chat("/commercial 60")
    cd[2] = 18000
    return cd


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


def puntos(msg, user):
    tipo = len(msg.split(" "))
    if tipo == 1:
        pts = Puntos.comprobar(user)
        if pts == -1:
            Sender.chat(f"/me Lo siento, {user}, pero aún no estás registrado. "
                        f"Por favor, comprueba la ayuda en !puntos ayuda")
        else:
            Sender.chat(f"/me {user}, tienes {pts} puntos.")
    elif tipo == 2 or tipo == 3:
        comando = msg.split(" ")[1]
        if comando == "ayuda":
            print("Comando no implementado")
        elif comando == "registrar":
            args = msg.split(" ")
            tipo = len(args)
            if tipo == 2:
                Puntos.registrar(user, user)
            elif tipo == 3:
                Puntos.registrar(user, args[2])
        elif comando == "perfil":
            args = msg.split(" ")
            tipo = len(args)
            if tipo == 2:
                perfil = Puntos.perfil_propio(user)
                equipo = Puntos.equipo(user)
                if perfil is None:
                    Sender.chat(f"/me Lo siento, {user}, pero aún no estás registrado. "
                                f"Por favor, comprueba la ayuda en !puntos ayuda")
                else:
                    if equipo is not None:
                        Sender.chat(
                            f"/me {user}, eres {perfil[0]} y tienes {perfil[1]} puntos. {equipo}")
                    else:
                        Sender.chat(
                            f"/me {user}, eres {perfil[0]} y tienes {perfil[1]} puntos.")
            elif tipo == 3:
                perfil = Puntos.perfil_ajeno(args[2])
                equipo = Puntos.equipo_ajeno(args[2])
                if perfil is None:
                    Sender.chat(f"/me Lo siento, {user}, pero no he encontrado al usuario que buscas.")
                else:
                    if equipo is not None:
                        Sender.chat(
                            f"/me {user}, {args[2]} es {perfil[0]} y tiene {perfil[1]} puntos. {equipo}")
                    else:
                        Sender.chat(
                            f"/me {user}, {args[2]} es {perfil[0]} y tiene {perfil[1]} puntos.")
        elif comando == "inventario":
            args = msg.split(" ")
            tipo = len(args)
            if tipo == 2:
                inventario = Puntos.inventario(user)
                if inventario is None:
                    Sender.chat(f"/me Lo siento, {user}, pero no tienes objetos en tu inventario.")
                else:
                    Sender.chat(f"/me {user}, tienes los siguientes objetos en tu inventario: {inventario}")
            elif tipo == 3:
                inventario = Puntos.inventario(args[2])
                if inventario is None:
                    Sender.chat(f"/me Lo siento, {user}, pero no he encontrado al usuario que buscas.")
                else:
                    Sender.chat(f"/me {user}, {args[2]} tiene los siguientes objetos en su inventario: {inventario}")
        elif comando == "tienda":
            tienda = Puntos.tienda()
            Sender.chat(f"/me {user}, los objetos de la tienda con sus precios son los siguientes: {tienda}")
        elif comando == "bunko":
            bunko = Puntos.bunko()
            Sender.chat(f"/me {user}, los objetos de EL BUNKO con sus precios son los siguientes: {bunko}")
