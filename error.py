import tkinter as tk
from tkinter import *
from tkinter import messagebox

import sys

def error_pop_up(error_title, error_message, kill_app = True):
    # Créer une fenêtre Tkinter vide
    window = Tk()

    # Cacher la fenêtre principale
    window.withdraw()

    # Afficher la fenêtre pop-up d'erreur
    messagebox.showerror("Alerte Médicale : " + error_title, error_message)

    # Fermer la fenêtre Tkinter
    if (kill_app):
        sys.exit(1)
    window.destroy()