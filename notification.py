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
    """
    Joue un son en boucle jusqu'à ce que l'événement d'arrêt soit défini.

    Cette fonction utilise la commande système `aplay` pour jouer le son situé à l'emplacement spécifié en boucle.
    Le son est joué en utilisant le périphérique audio spécifié ("hw:3,1") qui le périphérique de loopback créé.

    La fonction continue de jouer le son en boucle jusqu'à ce que l'événement d'arrêt (`stop_event`) soit défini.
    Lorsque l'événement d'arrêt est défini, la lecture du son s'arrête.

    Args:
        sound_path (str): Le chemin vers le fichier son à jouer.
        stop_event (threading.Event): L'événement d'arrêt pour contrôler la détection.
    """

    while not stop_event.is_set():
        os.system("aplay -D hw:3,1 " + sound_path)
        
def alert(title, msg_btn, image_path=None, msg_alert="Alerte détectée...", sound_path=None):
    """
    Affiche une fenêtre d'alerte avec un message et une option pour arrêter une notification sonore.

    Cette fonction crée une fenêtre d'alerte avec un titre spécifié et un message d'alerte.
    Elle peut également afficher une image en option et jouer une notification sonore en boucle.

    Args:
        title (str): Le titre de la fenêtre d'alerte.
        msg_btn (str): Le texte du bouton pour fermer la fenêtre d'alerte.
        image_path (str, optional): Le chemin vers une image à afficher dans la fenêtre d'alerte. Par défaut None.
        msg_alert (str, optional): Le message d'alerte à afficher dans la fenêtre d'alerte. Par défaut "Alerte détectée...".
        sound_path (str, optional): Le chemin vers un fichier audio à jouer en boucle lors de l'affichage de l'alerte. Par défaut None.
    """
    
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


