from pygame import mixer
import pygame
import platform
import os
import datetime

import logs
import sys

def play_sound(sound_path):
    try:
        mixer.init()
        mixer.music.load(sound_path)
        mixer.music.play()
    except pygame.error:
        print("[ERREUR 30]: Le fichier "+ sound_path + " est introuvable.\n")
        message = "\n" + "[ERREUR 30] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Le fichier "+ sound_path + " est introuvable."
        logs.write_daily_log(message)

def read_params():
    try:
        with open('params.txt', 'r') as file:
            # Lecture des lignes du fichier
            lignes = file.readlines()
    except FileNotFoundError :
        clear()
        print("[ERREUR 31]: Lancement de l'application impossible !\nFichier de paramètres non trouvé.\n")
        message = "\n" + "[ERREUR 31] : " + datetime.datetime.now().strftime("%H:%M:%S") + " - Lancement de l'application impossible !\nFichier de paramètres non trouvé."
        logs.write_daily_log(message)
        sys.exit(1)
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
    if platform.system() == "Windows":
        os.startfile(path)

    if platform.system() == "Linux":
        os.system(f"xdg-open {path}")

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    if platform.system() == "Linux":
        os.system('clear')
