from pygame import mixer
import platform
import os

def play_sound(sound_path):
    mixer.init()
    mixer.music.load(sound_path)
    mixer.music.play()

def read_params():
    with open('params.txt', 'r') as file:
        # Lecture des lignes du fichier
        lignes = file.readlines()

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
