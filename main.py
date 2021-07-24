import Log
import Comandos
from multiprocessing import Process

import Puntos
import TkInter


def func1():
    print('Iniciando log')
    Log.log()


def func2():
    print('Iniciando comprobación de comandos')
    Comandos.main()


def func3():
    print('Iniciando sistema de puntos')
    Puntos.main()


if __name__ == '__main__':
    users = []
    cd = []
    chat = open("logs/chat.txt", "w", encoding="utf-8")
    chat.write("")
    chat.close()
    log = open("logs/chat.log", "w", encoding="utf-8")
    log.write("")
    log.close()

    p1 = Process(target=func1)
    p2 = Process(target=func2)
    p3 = Process(target=func3)
    p1.start()
    p2.start()
    p3.start()

    TkInter.main()

    p1.terminate()
    print("Log terminado")
    p2.terminate()
    print("Comandos terminados")
    p3.terminate()
    print("Puntos terminados")
