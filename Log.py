import socket
import time

import config
import logging
from emoji import demojize


def log():
    print("Logging")
    sock = socket.socket()

    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'yastarth'
    token = config.oauth_token
    channel = '#yastme'

    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    f = open("chat.log", "w", encoding="utf-8")
    f.write("")
    f.close()

    x = 0

    while True:

        try:
            resp = sock.recv(2048).decode('utf-8')
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s — %(message)s',
                                datefmt='%Y-%m-%d_%H:%M:%S',
                                handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

            logging.info(resp)

            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))

            elif len(resp) > 0:
                logging.info(demojize(resp))
        except:
            time.sleep(x)
            x = x*2
