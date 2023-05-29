import datetime
import os
import sys

log_directory = "./logs"

def create_daily_log():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    log_path = os.path.join(log_directory, f"log_{today}.txt")
    if not os.path.exists(log_path):
        try:
            with open(log_path, 'w') as log_file:
                log_file.write(f"Log file for {today}\n")
        except FileNotFoundError:
            print("[ERREUR 20]: Le dossier d'historique est introuvable.\nChemin par défaut : ./logs")
            sys.exit(1)


def write_daily_log(message):
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
        print("[ERREUR 21]: Impossible d'enregistrer l'historique.\n")
        sys.exit(1)