from pygame import mixer
import pygame
import platform
import os
import threading
import datetime

import logs
import sys
import error

def play_sound_thread(sound_path):
    # Exécute la commande pour lire le fichier audio
    os.system("aplay -D hw:3,1 " + sound_path)


def play_sound(sound_path):
    try:
        if platform.system() == "Windows":
            mixer.init()
            mixer.music.load(sound_path)
            mixer.music.play()
        if platform.system() == "Linux":
            thread = threading.Thread(target=play_sound_thread, args=(sound_path,))
            thread.start()
    except pygame.error:
        message = "\n" + "[ERREUR 30] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Le fichier "+ sound_path + " est introuvable."
        logs.write_daily_log(message)
        error_title = "[ERREUR 30]"
        error_message = "Le fichier "+ sound_path + " est introuvable.\n"
        error.error_pop_up(error_title, error_message, False)

def read_params():
    try:
        with open('params.txt', 'r') as file:
            # Lecture des lignes du fichier
            lignes = file.readlines()
    except FileNotFoundError :
        clear()
        message = "\n" + "[ERREUR 31] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Lancement de l'application impossible !\nFichier de paramètres non trouvé."
        logs.write_daily_log(message)
        error_title = "[ERREUR 31]"
        error_message = "Lancement de l'application impossible !\nFichier de paramètres non trouvé.\n"
        error.error_pop_up(error_title, error_message)
    else:
        # Initialisation d'un dictionnaire pour stocker les valeurs de chaque variable globale
        variables_globales = {}

        # Analyse de chaque ligne du fichier pour extraire les valeurs de chaque variable globale
        for ligne in lignes:
            # Séparation de la ligne en fonction des virgules et des signes égal
            elements = ligne.strip().split('\n')
            for element in elements:
                nom, valeur = element.strip().split('=')
                # Ajout de la valeur extraite dans le dictionnaire des variables globales
                variables_globales[nom] = valeur
        return variables_globales

def open_folder(path):
    try:
        if platform.system() == "Windows":
            os.startfile(path)

        if platform.system() == "Linux":
            os.system(f"xdg-open {path}")
    except:
        error_title = "[ERREUR 31]"
        error_message = "Fichiers des paramètres non trouvé.\n"
        error.error_pop_up(error_title, error_message)

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    if platform.system() == "Linux":
        os.system('clear')

