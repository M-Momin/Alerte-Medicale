import datetime
import os
import sys

import error

log_directory = "./logs"

def create_daily_log():
    """
    Crée un fichier journal quotidien pour enregistrer les logs de l'application.

    Cette fonction crée un fichier journal quotidien pour enregistrer les logs de l'application. Le fichier journal
    est nommé en fonction de la date actuelle au format 'log_YYYY-MM-DD.txt' et est stocké dans le dossier des logs.
    Si le fichier journal pour la date actuelle n'existe pas, la fonction crée le fichier et écrit une ligne d'en-tête
    indiquant la date du journal.

    Si le dossier des logs n'existe pas, la fonction affiche une boîte de dialogue d'erreur.
    """
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    log_path = os.path.join(log_directory, f"log_{today}.txt")
    if not os.path.exists(log_path):
        try:
            with open(log_path, 'w') as log_file:
                log_file.write(f"Log file for {today}\n")
        except FileNotFoundError:
            error_title = "[ERREUR 20]"
            error_message = "Le dossier d'historique est introuvable.\nChemin par défaut : ./logs"
            error.error_pop_up(error_title, error_message)



def write_daily_log(message):
    """
    Écrit un message dans le fichier journal quotidien.

    Cette fonction écrit le message spécifié dans le fichier journal quotidien correspondant à la date actuelle.
    Le nom du fichier est généré en utilisant la date actuelle au format 'log_YYYY-MM-DD.txt' et est stocké dans le
    dossier des logs.

    Si le fichier journal n'existe pas, il est créé. Le message est ajouté à la fin du fichier, suivi d'un retour à la
    ligne.

    Si le dossier des logs n'existe pas ou s'il y a une erreur lors de l'écriture dans le fichier, la fonction affiche
    une boîte de dialogue d'erreur.

    Args:
        message (str): Le message à écrire dans le fichier journal.
    """
    
    # obtenir la date actuelle
    date_actuelle = datetime.datetime.now().strftime("%Y-%m-%d")

    # créer le nom de fichier correspondant à la date actuelle
    nom_fichier = f"./{log_directory}/log_{date_actuelle}.txt"

    # ouvrir le fichier en mode ajout (append)
    try:
        with open(nom_fichier, "a") as f:
            # écrire le message dans le fichier, suivi d'un retour à la ligne
            f.write(message + "\n")
    except FileNotFoundError:
        error_title = "[ERREUR 21]"
        error_message = "Impossible d'enregistrer l'historique."
        error.error_pop_up(error_title, error_message)

