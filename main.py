import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sound_detector
import threading
import os

import pyaudio

import struct

# Définir les paramètres audio
sample_format = pyaudio.paInt16
channels = 1
framerate = 7500
chunk_size = 2048

test = 0

event = threading.Event()
event.clear()

event_start = threading.Event()
event_start.clear()

event_stop= threading.Event()
event_stop.clear()

event_kill = threading.Event()
event_kill.clear()



if __name__ == "__main__":

        
    def long_running_function():
        #def brain():
        # Boucle d'enregistrement et de détection de la séquence de fréquences
        
        # Initialisation de l'enregistrement audio
        audio = pyaudio.PyAudio()
        stream = audio.open(format=sample_format,
                            channels=channels,
                            rate=framerate,
                            input=True,
                            frames_per_buffer=chunk_size)
        while True:
            if event_start.is_set():
                print("stream lancé")
                stream.start_stream()
                event_start.clear()

            if event_stop.is_set():
                print("stream stoppé")
                stream.stop_stream()
                event_stop.clear()
                
            if(event_kill.is_set()):
                break
            # Lecture des échantillons audio du microphone
            data = stream.read(chunk_size)
            format_string = '<{}h'.format(chunk_size)
            waveform = struct.unpack(format_string, data)
            
            sound_detector.High_SG(sound_detector.target_frequencies_High_SG, waveform)
            sound_detector.Low_SG(sound_detector.target_frequencies_Low_SG, waveform)
            
            event.wait()
                
        # Arrêt de l'enregistrement audio
        stream.stop_stream()
        stream.close()
        audio.terminate()

        return 0
    # Définition de la fonction à exécuter lorsque le bouton est cliqué
    def surveillance_on():
        event.set()
        event_start.set()
 
        root.configure(bg="green")
        # Création d'une nouvelle thread pour exécuter la fonction
        t = threading.Thread(target=long_running_function)
        t.start()
        surveillance_btn.configure(text = "Désactivé\nSurveillance ?", command=surveillance_off)
        state_label.configure(text="✔️ Surveillance ON",borderwidth=1, relief="solid", fg="green")
        os.system('cls')
        print("La surveillance a été activée. \n\n En cours d'écoute ... \n\n")

    def surveillance_off():
        event.clear()
        event_stop.set()
        
        root.configure(bg="red")
        surveillance_btn.configure(text = "Activé\nSurveillance ?", command=surveillance_on)
        state_label.configure(text="❌ Surveillance OFF",borderwidth=1, relief="solid", fg="red")
        os.system('cls')
        print("La surveillance a été désactivée. \n\n")


    def quitWin():
        res = messagebox.askyesno('prompt', 'Voulez-vous fermer cette fenêtre?') 
        if res == True:
            event_kill.set()
            event.set()
            root.destroy()

        elif res == False:
            pass
        else:
            messagebox.showerror('error', 'something went wrong!')

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            event_kill.set()
            event.set()
            root.destroy()

    # Création de la fenêtre principale
    os.system('cls')

    os.system( 'title Alerte Médicale : Gestionnaire' )
    cmd = 'color 3F' 
    os.system(cmd)
    cmd = 'mode 67, 30'
    os.system(cmd)
    print("Running ...")

    root = tk.Tk()
    root.title("Alerte Médicale !")
    root.geometry('875x585')
    root.resizable(0, 0)
    # Définition de la fonction à exécuter dans une nouvelle thread
    
    background_image = tk.PhotoImage(file="./images/bg_1.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    state_label = Label(root, text="❌Surveillance OFF", width=20, height=2, font=("Arial", 18), borderwidth=1, relief="solid", fg="red",activebackground="white")
    state_label.pack()
    state_label.place(x=550, y= 30)

    surveillance_btn = Button(root, text="Activé\nSurveillance ?", width=17, height=2, font=("Arial", 12), command=surveillance_on)
    surveillance_btn.pack(pady=15)
    surveillance_btn.place(x=300, y=200)

    logs_btn = Button(root, text="Historique", width=17, height=2, font=("Arial", 12))
    logs_btn.pack(pady=15)
    logs_btn.place(x=300, y=275)

    settings_btn = Button(root, text="Réglages", width=17, height=2, font=("Arial", 12))
    settings_btn.pack(pady=15)
    settings_btn.place(x=300, y=350)

    quit_btn = Button(root, text="Quitter", command=quitWin, width=10, height=1, font=("Arial", 10))
    quit_btn.pack(pady=100)
    quit_btn.place(x=750, y=525)

    # Lancement de la boucle principale de tkinter pour afficher la fenêtre
    root.protocol("WM_DELETE_WINDOW", on_closing)
    test = root
    root.mainloop()

