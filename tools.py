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
    """
    Joue un fichier audio.

    Cette fonction joue le fichier audio spécifié par `sound_path` en utilisant les fonctionnalités appropriées en fonction du système d'exploitation.
    Si le système d'exploitation est Windows, la fonction `mixer.music` de la bibliothèque `pygame` est utilisée pour jouer le son.
    Si le système d'exploitation est Linux, un thread est créé pour exécuter la fonction `play_sound_thread` qui joue le son à l'aide de la commande système appropriée.

    Args:
        sound_path (str): Chemin vers le fichier audio à jouer.

    Raises:
        Exception: Si une erreur se produit lors de la lecture du fichier audio.
    """

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
    """
    Lit les paramètres à partir d'un fichier texte et les stocke dans un dictionnaire.

    Cette fonction lit le fichier `params.txt` qui contient les paramètres sous la forme de lignes contenant des noms de variables et leurs valeurs.
    Chaque ligne est analysée pour extraire le nom et la valeur de chaque variable, puis ces valeurs sont stockées dans un dictionnaire.
    Si le fichier `params.txt` n'est pas trouvé, une erreur est affichée.

    Returns:
        dict: Dictionnaire contenant les valeurs de chaque variable globale.

    Raises:
        FileNotFoundError: Si le fichier `params.txt` n'est pas trouvé.
    """
    
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
    """
    Ouvre un dossier à l'emplacement spécifié.

    Cette fonction ouvre le dossier situé à l'emplacement `path` en utilisant les commandes système appropriées en fonction du système d'exploitation.
    Si le système d'exploitation est Windows, la fonction `os.startfile` est utilisée pour ouvrir le dossier.
    Si le système d'exploitation est Linux, la fonction `os.system` est utilisée avec la commande `xdg-open` pour ouvrir le dossier.

    Args:
        path (str): Chemin vers le dossier à ouvrir.

    Raises:
        Exception: Si une erreur se produit lors de l'ouverture du dossier.
    """

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

