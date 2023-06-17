import tkinter as tk
from tkinter import *
from tkinter import messagebox

import sys

def error_pop_up(error_title, error_message, kill_app = True):
    """
    Affiche une fenêtre de notification d'erreur avec un titre et un message donné.
    
    Args :
    error_title -> Le titre de l'erreur affiché dans la fenêtre pop-up
    error_message -> Le message d'erreur à afficher dans la fenêtre pop-up
    kill_app -> Indique si l'application doit être arrêtée après l'affichage de la fenêtre pop-up (par défaut True)
    """

    # Initialise une fenêtre Tkinter
    window = Tk()

    # Cache la fenêtre Tkinter
    window.withdraw()

    # Affiche une fenêtre pop-up d'erreur
    messagebox.showerror("Alerte Médicale : " + error_title, error_message)

    # Ferme la fenêtre Tkinter
    if (kill_app):
        sys.exit(1)
    window.destroy()