import config


def parse():
    chat_log = open('logs/chat.log', "r", encoding="utf-8")
    chat = chat_log.read().split("\n\n\n")
    chat_parsed = open("logs/chat.txt", "w", encoding="utf-8")
    lines = []
    try:
        for i in chat:
            if len(i) > 0:
                if "GLHF!" not in i:
                    if "PING" not in i:
                        if config.nickname != i.split(":")[2] and config.nickname != i.split(":")[4] \
                                and f"{config.nickname} = #{config.channel}" not in i.split("—")[1].split(":")[2]:
                            if len(i) > 0:
                                user = f"{i.split('—')[1].split(':')[1].split('!')[0]}"
                                msg = f"{i.split('—')[1].split(':')[2]}"
                                line = str(user + " — " + msg)
                                lines.append(line)

        for i in lines:
            chat_parsed.write(str(i))
            chat_parsed.write('\n')
        chat_log.close()
        chat_parsed.close()
    except IndexError:
        pass
