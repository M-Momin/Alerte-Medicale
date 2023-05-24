import tkinter as tk
from tkinter import *
from tkinter import messagebox
import main

class BlinkingLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.color = 'red'
        self.bgcolor = 'white'
        self.after(500, self.blink)

    def blink(self):
        if self.color == 'white':
            self.color = 'red'
            self.bgcolor = 'white'
        else:
            self.color = 'white'
            self.bgcolor = 'red'
        self.config(fg=self.color, bg=self.bgcolor)
        self.after(1000, self.blink)


def alert(title, msg_btn, image_path=None, msg_alert="Alerte détectée..."):
    root = tk.Toplevel(main.root_send)
    root.title(title)
    root.geometry('750x422')
    root.resizable(0, 0)
    root.config(bg='red2')

    if image_path:
        background_image = tk.PhotoImage(file=image_path)
        background_label = tk.Label(root, image=background_image)
        background_label.place(relwidth=1, relheight=1)

    def quitWin():
        root.destroy()

    close_btn = Button(root, text=msg_btn, command=quitWin, width=6, height=1,font=("Arial", 11))
    close_btn.pack()
    close_btn.place(x= 665, y=375)

    state_label_alert = BlinkingLabel(root, text=msg_alert, font=("Arial", 15), width = 32, height = 2,borderwidth=1, relief="solid", fg="red")
    state_label_alert.pack()
    state_label_alert.place(x=200, y=185)


    # Attendre que la fenêtre soit fermée
    root.wait_window()