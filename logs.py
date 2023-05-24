import datetime
import os

log_directory = "./logs"

def create_daily_log():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    log_path = os.path.join(log_directory, f"log_{today}.txt")
    if not os.path.exists(log_path):
        with open(log_path, 'w') as log_file:
            log_file.write(f"Log file for {today}\n")

def write_daily_log(message):
    # obtenir la date actuelle
    date_actuelle = datetime.datetime.now().strftime("%Y-%m-%d")

    # créer le nom de fichier correspondant à la date actuelle
    nom_fichier = f"./{log_directory}/log_{date_actuelle}.txt"

    # ouvrir le fichier en mode ajout (append)
    with open(nom_fichier, "a") as f:
        # écrire le message dans le fichier, suivi d'un retour à la ligne
        f.write(message + "\n")