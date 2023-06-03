import tkinter as tk
from tkinter import Tk, Button, Label, PhotoImage
from tkinter import *
from tkinter import messagebox
import platform
import tools
import os
import threading
import pygame


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


def play_sound_in_loop(sound_path, stop_event):
    while not stop_event.is_set():
        os.system("aplay -D hw:3,1 " + sound_path)
        
def alert(title, msg_btn, image_path=None, msg_alert="Alerte détectée...", sound_path=None):
    global event_kill

    if sound_path:
        if platform.system() == "Windows":
            pygame.init()
            # Chargement du son
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(-1)
            
        if platform.system() == "Linux":
            stop_event = threading.Event()
            sound_thread = threading.Thread(target=play_sound_in_loop, args=(sound_path, stop_event))
            sound_thread.start()
        
    alert_notif = Tk()
    alert_notif.title(title)
    alert_notif.geometry('750x422')
    alert_notif.resizable(0, 0)
    alert_notif.config(bg='#ccfff5')      
    
    def quitWin():
        
        if sound_path:
            if platform.system() == "Linux":
                stop_event.set()  # Définir l'événement pour arrêter le thread
            if platform.system() == "Windows":
                pygame.mixer.music.stop()  
        alert_notif.destroy()

    close_btn = Button(alert_notif, text=msg_btn, command=quitWin, width=6, height=1, font=("Arial", 11))
    close_btn.pack()
    close_btn.place(x=665, y=375)
    
    state_label_alert = BlinkingLabel(alert_notif, text=msg_alert, font=("Arial", 15), width=32, height=2,
                                      borderwidth=1, relief="solid", fg="red")
    state_label_alert.pack()
    state_label_alert.place(x=200, y=185)

    alert_notif.wait_window()


