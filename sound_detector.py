import pyaudio

import struct
import math
import threading
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
import blinking
import main

# Paramètres de la séquence de fréquences à détecter
target_frequencies_High_SG = [1312, 1410, 1500, 1619, 1722]
target_frequencies_Low_SG = [1722, 1619, 1500, 1410, 1312]
threshold = 0.15 # Seuil de corrélation minimum


# Paramètres du microphone
#chunk_size = 1024
#sample_format = pyaudio.paInt16
#channels = 1
#framerate = 44100

# Définir les paramètres audio
sample_format = pyaudio.paInt16
channels = 1
framerate = 7500
chunk_size = 512


detected_list_High_SG = [];
last_freq_High_SG = 0;
detected_list_Low_SG = [];
last_freq_Low_SG = 0;


def test_alert(title, msg_btn, image_path=None, msg_alert="Alerte détectée..."):
    root = tk.Toplevel(main.test)
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

    state_label_alert = blinking.BlinkingLabel(root, text=msg_alert, font=("Arial", 15), width = 32, height = 2,borderwidth=1, relief="solid", fg="red")
    state_label_alert.pack()
    state_label_alert.place(x=200, y=185)


    # Attendre que la fenêtre soit fermée
    root.wait_window()



# Fonction pour calculer la corrélation entre deux formes d'onde
def calculate_correlation(waveform1, waveform2):
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    for x, y in zip(waveform1, waveform2):
        sum_xy += x * y
        sum_x2 += x ** 2
        sum_y2 += y ** 2
    correlation = sum_xy / math.sqrt(sum_x2 * sum_y2)
    return correlation

def High_SG(target, waveform):
    global detected_list_High_SG
    global last_freq_High_SG
    # Calcul de la corrélation entre la forme d'onde et chaque fréquence cible
    correlations = []
    for freq in target: #target_frequencies_High_SG:
        reference_waveform = [int(32767.0 * math.sin(2.0 * math.pi * freq * t / framerate)) for t in range(chunk_size)]
        correlation = calculate_correlation(waveform, reference_waveform)
        correlations.append(correlation)

    # Détection de la fréquence correspondant à la plus forte corrélation
    max_correlation = max(correlations)
    max_index = correlations.index(max_correlation)
    max_freq = target[max_index]

    # Affichage de la fréquence détectée si la corrélation est suffisante
    if max_correlation >= threshold:
        if len(detected_list_High_SG) > 5:
            detected_list_High_SG = []
        if last_freq_High_SG != max_freq:
            print(datetime.datetime.now().strftime("%H:%M:%S"), 'HSG_FR_Detected : {} Hz'.format(max_freq))
            detected_list_High_SG.append(max_freq)
            last_freq_High_SG = max_freq
            if max_freq == target[4]:
                if target == detected_list_High_SG:
                    print(datetime.datetime.now().strftime("%H:%M:%S"),"\n\n       !!!!!!!!!!!! Alerte : High_SG  !!!!!!!!!!!!       \n\n")
                    #alert_popup = threading.Thread(target=test_alert("Alerte High SG!", "Ok !", "./images/alerte_v2.png", "Une alerte HIGH SG a été détectée ..."))
                    #alert_popup.start()
                    test_alert("Alerte High SG!", "Ok !", "./images/alerte_v2.png", "Une alerte HIGH SG a été détectée ...")
                detected_list_High_SG = []


def Low_SG(target, waveform):
    # Calcul de la corrélation entre la forme d'onde et chaque fréquence cible
    global detected_list_Low_SG
    global last_freq_Low_SG
    correlations = []
    for freq in target: #target_frequencies_Low_SG:
        reference_waveform = [int(32767.0 * math.sin(2.0 * math.pi * freq * t / framerate)) for t in range(chunk_size)]
        correlation = calculate_correlation(waveform, reference_waveform)
        correlations.append(correlation)

    # Détection de la fréquence correspondant à la plus forte corrélation
    max_correlation = max(correlations)
    max_index = correlations.index(max_correlation)
    max_freq = target[max_index]

    # Affichage de la fréquence détectée si la corrélation est suffisante
    if max_correlation >= threshold:
        print(datetime.datetime.now().strftime("%H:%M:%S"), 'LSG_FR_Detected : {} Hz'.format(max_freq))
    '''   if len(detected_list_Low_SG) > 5:
            detected_list_Low_SG = []
        if last_freq_Low_SG != max_freq:
            print(datetime.datetime.now().strftime("%H:%M:%S"), 'LSG_FR_Detected : {} Hz'.format(max_freq))
            detected_list_Low_SG.append(max_freq)
            last_freq_Low_SG = max_freq
            if max_freq == target[4]:
                if target == detected_list_Low_SG:
                    print("\n\n       !!!!!!!!!!!! Alerte : Low_SG  !!!!!!!!!!!!       \n\n")
                    #alert_popup = threading.Thread(target=test_alert("Alerte Low SG!", "Ok !", "./images/bg_alert_warning_2.png", "Une alerte LOW SG a été détectée ..."))
                    #alert_popup.start()
                    test_alert("Alerte Low SG!", "Ok !", "./images/bg_alert_warning_2.png", "Une alerte LOW SG a été détectée ...")
                detected_list_Low_SG = []'''


def brain():
    # Initialisation de l'enregistrement audio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=sample_format,
                        channels=channels,
                        rate=framerate,
                        input=True,
                        frames_per_buffer=chunk_size)



    # Boucle d'enregistrement et de détection de la séquence de fréquences
    '''while True:
        if mevent.is_set():
            print("set")
        else:
            print("not set")
        main.event.wait()
        # Lecture des échantillons audio du microphone
        data = stream.read(chunk_size)
        format_string = '<{}h'.format(chunk_size)
        waveform = struct.unpack(format_string, data)
        
        #High_SG(target_frequencies_High_SG, waveform)
        Low_SG(target_frequencies_Low_SG, waveform)
        #thread1 = threading.Thread(target=High_SG(target_frequencies_High_SG, waveform))
        #thread2 = threading.Thread(target=Low_SG(target_frequencies_Low_SG, waveform))

        # démarrer les threads
        #thread1.start()
        #thread2.start()
        

        # attendre que les threads se terminent
        #thread1.join()
        #thread2.join()

            
    # Arrêt de l'enregistrement audio
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return 0'''
