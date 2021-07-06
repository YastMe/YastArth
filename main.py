import Log
import Comandos
from multiprocessing import Process
import TkInter


def func1():
    print('Iniciando log')
    Log.log()


def func2():
    print('Iniciando comprobación de comandos')
    Comandos.main()


if __name__ == '__main__':
    users = []
    cd = []
    chat = open("chat.txt", "w", encoding="utf-8")
    chat.write("")
    chat.close()
    log = open("chat.log", "w", encoding="utf-8")
    log.write("")
    log.close()

    p1 = Process(target=func1)
    p2 = Process(target=func2)
    p1.start()
    p2.start()

    TkInter.main()

    p1.terminate()
    print("Log terminado")
    p2.terminate()
    print("Comandos terminados")
