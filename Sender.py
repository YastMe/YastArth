import socket
import config


def chat(msg):
    sock = socket.socket()
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = config.nickname
    token = config.oauth_token
    channel = f'#{config.channel}'

    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))
    sock.send(f"PRIVMSG {channel} :{msg}\r\n".encode("utf-8"))


def PONG():
    sock = socket.socket()
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = config.nickname
    token = config.oauth_token
    channel = f'#{config.channel}'

    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))
    sock.send("PONG".encode("utf-8"))
