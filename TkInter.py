import tkinter
import Sender


def winconfig(root):
    root.title("YastArth")
    root.geometry("700x100+50+50")
    root.resizable(width="False", height="False")


def btnconfig(root):
    global msg
    msg = tkinter.Entry(root)
    msg.place(x=100, y=50, width=400, height=20)
    btn = tkinter.Button(root, text="Enviar", command=lambda msg_send=msg: send(msg_send))
    btn.place(x=520, y=45)
    btn_exit = tkinter.Button(root, text="X", command=root.quit)
    btn_exit.place(x=675, y=10)


def send(event):
    Sender.chat(msg.get())
    msg.delete(0, 'end')
    msg.update()


def main():
    root = tkinter.Tk()
    winconfig(root)
    btnconfig(root)
    root.bind('<Return>', send)
    root.mainloop()
