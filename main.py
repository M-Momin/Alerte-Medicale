import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

import sound_detector
import logs
import tools

import threading
import os
import sys
import time
import platform
import datetime

import pyaudio

import struct

variables_globales = tools.read_params()

# Définir les paramètres audio
global sample_format, channels, framerate, chunk_size, threshold, target_frequencies_High_SG, target_frequencies_Low_SG, target_frequencies_Alert_SG

tools.clear()

sample_format = pyaudio.paInt16
try:
    channels = int(variables_globales['channels'])
except ValueError:
    print("[Erreur]: la valeur par défaut de 'channels' doit être de type 'int'. \nValeur par défaut : 1")
    sys.exit(1)
try:  
    framerate = int(variables_globales['framerate'])
except ValueError:
    print("[Erreur]: la valeur par défaut de 'framerate' doit être de type 'int'. \nValeur par défaut : 7500")
    sys.exit(1)
try:
    chunk_size = int(variables_globales['chunk_size'])
except ValueError:
    print("[Erreur]: la valeur par défaut de 'channels' doit être de type 'int'. \nValeur par défaut : 256")
    sys.exit(1)
try:
    threshold = float(variables_globales['threshold'])/1000
except ValueError:
    print("[Erreur]: la valeur par défaut de 'channels' doit être de type 'int'. \nValeur par défaut : 35")
    sys.exit(1)
try:
    target_frequencies_High_SG = eval(variables_globales['target_frequencies_High_SG'])
except SyntaxError:
    print("[Erreur]: la valeur par défaut de 'channels' doit être de type 'tableau'. \nValeur par défaut : [1312, 1410, 1500, 1619, 1722]")
    sys.exit(1)
try:
    target_frequencies_Low_SG = eval(variables_globales['target_frequencies_Low_SG'])
except SyntaxError:
    print("[Erreur]: la valeur par défaut de 'channels' doit être de type 'tableau'. \nValeur par défaut : [1722, 1619, 1500, 1410, 1312]")
    sys.exit(1)
try:
    target_frequencies_Alert_SG = eval(variables_globales['target_frequencies_Alert_SG'])
except SyntaxError:
    print("[Erreur]: la valeur par défaut de 'channels' doit être de type 'tableau'. \nValeur par défaut : [1655, 3310, 1655, 3310, 1655, 3310]")
    sys.exit(1)


root_send = 0

first_start = True

event = threading.Event()
event.clear()

event_start = threading.Event()
event_start.clear()

event_stop= threading.Event()
event_stop.clear()

event_kill = threading.Event()
event_kill.clear()



if __name__ == "__main__":
    logs.create_daily_log()
    message = "\n" + "[État] : " +datetime.datetime.now().strftime("%H:%M:%S") + " - Le programme à démarré.\n"
    logs.write_daily_log(message)


    def long_running_function():
        global first_start
        audio = pyaudio.PyAudio()

        # Initialisation de l'enregistrement audio

        try:
            stream = audio.open(format=sample_format,
                                channels=channels,
                                rate=framerate,
                                input=True,
                                frames_per_buffer=chunk_size)
        except OSError as e:
            surveillance_off("[ERREUR] : Erreur d'ouverture de flux de données.")
            message = "\n" + "[ERREUR] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Erreur d'ouverture de flux de données.\n"
            logs.write_daily_log(message)



        while True:

            if event_start.is_set():
                try:
                    stream.start_stream()
                except (NameError, UnboundLocalError) as e:
                    pass
                else:
                    try:
                        info = audio.get_default_input_device_info()
                    except OSError as e:
                        surveillance_off("[ERREUR] : Périphérique de lecture manquant.")
                        message = "\n" + "[ERREUR] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Périphérique de lecture manquant.\n"
                        logs.write_daily_log(message)
                    else:
                        print("Micro utilisé : %s" % info['name'])
                        print("Enregistrement en cours...")
                    event_start.clear()



            if event_stop.is_set():
                try:
                    stream.stop_stream()
                except (NameError, UnboundLocalError, OSError) as e:
                    surveillance_off("[ERREUR] : Flux de lecture de données manquant.")
                    message = "\n" + "[ERREUR] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Flux de lecture de données manquant.\n"
                    logs.write_daily_log(message)
                else:
                    event_stop.clear()

                
            if(event_kill.is_set()):
                break

            # Lecture des échantillons audio du microphone
            try:
                data = stream.read(chunk_size)
                format_string = '<{}h'.format(chunk_size)
                waveform = struct.unpack(format_string, data)
                sound_detector.High_SG(target_frequencies_High_SG, waveform,sample_format,channels, float(threshold), chunk_size,framerate)
                sound_detector.Low_SG(target_frequencies_Low_SG, waveform,sample_format,channels, float(threshold), chunk_size, framerate)
                sound_detector.Alert_SG(target_frequencies_Alert_SG, waveform,sample_format,channels, float(threshold), chunk_size, framerate)

            except (UnboundLocalError, OSError) as e:
                if str(e) == "[Errno -9983] Stream is stopped":
                    surveillance_off("[ERREUR] : Lecture des données stoppée.")
                    message = "\n" + "[ERREUR] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Lecture des données stoppée..\n"
                    logs.write_daily_log(message)
                else:
                    surveillance_off("[ERREUR] : Erreur lors de la lecture des données.")
                    message = "\n" + "[ERREUR] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Erreur lors de la lecture des données.\n"
                    logs.write_daily_log(message)

                

            event.wait()
                
        # Arrêt de l'enregistrement audio
        try:
            stream.stop_stream()
            stream.close()
            audio.terminate()
        except UnboundLocalError:
            pass

        return 0

    # Définition de la fonction à exécuter lorsque le bouton est cliqué
    def surveillance_on():
        global first_start
        tools.clear()
        print("La surveillance est active ! \n\n")

        event.set()
        event_stop.clear()
        event_start.set()
        
        root.configure(bg="green")
        # Création d'une nouvelle thread pour exécuter la fonction
        if(first_start == True):
            t = threading.Thread(target=long_running_function)
            t.start()
            first_start= False
        surveillance_btn.configure(text = "Désactivé\nSurveillance  ", command=surveillance_off)
        state_label.configure(text="✔️ Surveillance ON", fg="green", bg="#d6f5d6")


    def surveillance_off(error =""):
        tools.clear()

        if(error != ""):
            print("La surveillance ne peut pas s'activer dû à une erreur : \n" + error + "\n\n  -> Vérifier votre périphérique d'enregistrement et ensuite \n     redémarrez l'application.")
        else:
            print("La surveillance est désactivée ! \n\n")

        event.clear()
        event_start.clear()
        event_stop.set()
        
        try:
            root.configure(bg="#ff704d")
            surveillance_btn.configure(text = "Activé\nSurveillance  ", command=surveillance_on)
            state_label.configure(text="❌ Surveillance OFF", fg="red", bg="#ffd6cc")
        except RuntimeError:
            pass

        
        

    def set_threshold_value(new_value):
        global threshold
        threshold = int(new_value)/1000

    def quitWin():
        res = messagebox.askyesno('Quitter ?', 'Voulez-vous quitter l\'application?') 
        if res == True:
            message = '\n' + "[État] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Le programme s'est éteint.\n"
            logs.write_daily_log(message)
            event_kill.set()
            event.set()
            root.destroy()
        elif res == False:
            pass
        else:
            messagebox.showerror('error', 'Un problème est survenu!')

    def on_closing():
        if messagebox.askokcancel("Quit", "Voulez-vous vraiment quitter ?"):
            message = '\n' + "[État] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Le programme s'est éteint.\n"
            logs.write_daily_log(message)
            event_kill.set()
            event.set()
            root.destroy()



    if platform.system() == "Windows":
        # Création de la fenêtre principale
        os.system('cls')

        os.system( 'title Alerte Médicale : Gestionnaire' )
        cmd = 'color 3F' 
        os.system(cmd)
        cmd = 'mode 67, 30'
        os.system(cmd)
    if platform.system() == "Linux":
        os.system('clear')

    print("En attente ...")



    root = tk.Tk()

    root.title("Alerte Médicale !")
    root.geometry('875x585')
    root.resizable(0, 0)
    # Définition de la fonction à exécuter dans une nouvelle thread


    background_image = tk.PhotoImage(file="./images/bg_1.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    state_label = Label(root, text="❌Surveillance OFF", width=20, height=2, font=("Helvetica", 18), fg="red",activebackground="#ff704d", bg="#ffd6cc")
    state_label.pack()
    state_label.place(x=550, y= 30)


    # Chargement de l'image
    image_power = Image.open("./images/power.png")
    image_power = image_power.resize((30, 30)) 
    photo_power = ImageTk.PhotoImage(image_power)
    # Création du bouton
    surveillance_btn = Button(root, text="Activé\nSurveillance  ", image=photo_power, width=160, height=50, compound="right", font=("Helvetica", 12), command=surveillance_on, highlightcolor="yellow")
    # Configuration du style personnalisé
    surveillance_btn.configure(bg="#eff5f5", fg="black", borderwidth=1, relief="solid")
    # Placement du bouton
    surveillance_btn.pack(pady=15)
    surveillance_btn.place(x=300, y=200)

    image_history = Image.open("./images/history.png")
    image_history = image_history.resize((25, 25)) 
    photo_history = ImageTk.PhotoImage(image_history)
    logs_btn = Button(root, text="Historique     ", width=160, height=50,compound="right", image=photo_history, font=("Helvetica", 12), command=lambda: tools.open_folder('logs'))
    logs_btn.configure(bg="#eff5f5", fg="black", borderwidth=1, relief="solid")
    logs_btn.pack(pady=15)
    logs_btn.place(x=300, y=275)

    image_settings = Image.open("./images/settings.png")
    image_settings = image_settings.resize((25, 25)) 
    photo_settings = ImageTk.PhotoImage(image_settings)
    settings_btn = Button(root, text="Réglages    ", width=160, height=50,compound="right", image=photo_settings, font=("Helvetica", 12), command=lambda: tools.open_folder('params.txt'))
    settings_btn.configure(bg="#eff5f5", fg="black", borderwidth=1, relief="solid")
    settings_btn.pack(pady=15)
    settings_btn.place(x=300, y=350)

    # Création du titre
    title_label = Label(root, text="Alarmes de tests :", font=("Helvetica", 11), foreground="black")
    title_label.pack(pady=10)
    title_label.place(x=700, y=200)

    image_volume = Image.open("./images/volume.png")
    image_volume = image_volume.resize((15, 15)) 
    photo_volume = ImageTk.PhotoImage(image_volume)
    test_LOW_btn = Button(root, text="Alarme Hypo   ", width=120, height=30, font=("Helvetica", 10),compound="right", image=photo_volume, command=lambda: tools.play_sound('./alarmes/LOW.wav'))
    test_LOW_btn.configure(bg="#eff5f5", fg="black", borderwidth=1, relief="solid")
    test_LOW_btn.pack(pady=15)
    test_LOW_btn.place(x=700, y=240)

    test_HIGH_btn = Button(root, text="Alarme Hyper   ", width=120, height=30, font=("Helvetica", 10),compound="right", image=photo_volume, command=lambda: tools.play_sound('./alarmes/HIGH.wav'))
    test_HIGH_btn.configure(bg="#eff5f5", fg="black", borderwidth=1, relief="solid")
    test_HIGH_btn.pack(pady=15)
    test_HIGH_btn.place(x=700, y=290)

    test_ALERT_btn = Button(root, text="Alarme Alerte   ", width=120, height=30, font=("Helvetica", 10),compound="right", image=photo_volume, command=lambda: tools.play_sound('./alarmes/ALERT.wav'))
    test_ALERT_btn.configure(bg="#eff5f5", fg="black", borderwidth=1, relief="solid")
    test_ALERT_btn.pack(pady=15)
    test_ALERT_btn.place(x=700, y=340)

    image_quit = Image.open("./images/quit.png")
    image_quit = image_quit.resize((15, 15)) 
    photo_quit = ImageTk.PhotoImage(image_quit)
    quit_btn = Button(root, text="Quitter   ", command=quitWin, width=80, height=20, font=("Helvetica", 10),compound="right", image=photo_quit)
    quit_btn.configure(bg="#eff5f5", fg="black", borderwidth=1, relief="solid")
    quit_btn.pack(pady=100)
    quit_btn.place(x=750, y=525)


    # Créer le curseur
    threshold_scale = tk.Scale(root, from_=1, to=100, resolution=1,  orient=tk.HORIZONTAL, command=set_threshold_value, label="Sensibilité :", bg="#eff5f5")
    # Afficher le curseur
    threshold_scale.set(threshold*1000)
    threshold_scale.pack()
    threshold_scale.place(x=510, y=200)

    # Lancement de la boucle principale de tkinter pour afficher la fenêtre
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root_send = root

    root.mainloop()

