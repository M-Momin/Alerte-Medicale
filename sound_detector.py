import struct
import math
import datetime

import logs
import notification


detected_list_High_SG = [];
last_freq_High_SG = 0;
detected_list_Low_SG = [];
last_freq_Low_SG = 0;
detected_list_Alert_SG = [];
last_freq_Alert_SG = 0;

last_freq = 0;
detected_list = [];

# Fonction pour calculer la corrélation entre deux formes d'onde
def calculate_correlation(waveform1, waveform2):
    """
    Calcule la corrélation entre deux formes d'onde.

    Cette fonction calcule la corrélation entre deux formes d'onde en utilisant la méthode de corrélation croisée.

    Args:
        waveform1 (list): Liste des valeurs de la première forme d'onde.
        waveform2 (list): Liste des valeurs de la deuxième forme d'onde.

    Returns:
        float: Valeur de corrélation normalisée entre -1.0 et 1.0.

    Exemple:
        waveform1 = [0.1, 0.2, 0.3, 0.4, 0.5]
        waveform2 = [0.2, 0.3, 0.4, 0.5, 0.6]
        correlation = calculate_correlation(waveform1, waveform2)
        print(correlation)
        # Résultat: 0.9999999999999998
    """
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    for x, y in zip(waveform1, waveform2):
        sum_xy += x * y
        sum_x2 += x ** 2
        sum_y2 += y ** 2
    correlation = sum_xy / math.sqrt(sum_x2 * sum_y2)
    return correlation


def High_SG(target, waveform,sample_format,channels, threshold, chunk_size, framerate):
    """
    Effectue la détection des fréquences dans une forme d'onde donnée pour les signaux de haute fréquence.

    Cette fonction compare la forme d'onde donnée avec une liste de fréquences cibles pour détecter la fréquence dominante correspondante.
    La corrélation est calculée entre la forme d'onde et chaque fréquence cible, et la fréquence avec la corrélation maximale est détectée.
    Si la corrélation dépasse le seuil donné, la fréquence détectée est affichée, et si toutes les fréquences cibles sont détectées dans l'ordre,
    une alerte "HYPER" est déclenchée.

    Args:
        target (list): Liste des fréquences cibles à détecter.
        waveform (list): Forme d'onde à analyser sous forme de liste de valeurs d'amplitude.
        sample_format (int): Format d'échantillonage des valeurs d'amplitude.
        channels (int): Nombre de canaux audio.
        threshold (float): Seuil de corrélation pour la détection de fréquence.
        chunk_size (int): Taille de chaque chunk de la forme d'onde pour le calcul de corrélation.
        framerate (int): Taux d'échantillonnage de la forme d'onde.
    """
    
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
        if last_freq_High_SG != max_freq:                
            print(datetime.datetime.now().strftime("%H:%M:%S"), 'HIGH_Info  : Fréquence détectée : {} Hz'.format(max_freq))
            detected_list_High_SG.append(max_freq)
            last_freq_High_SG = max_freq
            if len(detected_list_High_SG) == len(target):
                if target == detected_list_High_SG:
                    print(datetime.datetime.now().strftime("%H:%M:%S"),"\n\n              !!!!!!!!!!!! Alerte : HYPER !!!!!!!!!!!!       \n\n")
                    notification.alert("Alerte HYPER!", "Ok !", "./images/alerte_v2.png", "Une alerte HYPER a été détectée ...", "./alarmes/HIGH.wav")
                    message = datetime.datetime.now().strftime("%H:%M:%S") + " ---------------- >  Alerte HYPER détectée < ---------------- "
                    logs.write_daily_log(message)
                detected_list_High_SG = detected_list_High_SG[1:]



def Low_SG(target, waveform, sample_format,channels, threshold, chunk_size, framerate):
    """
    Effectue la détection des fréquences dans une forme d'onde donnée pour les signaux de basse fréquence.

    Cette fonction compare la forme d'onde donnée avec une liste de fréquences cibles pour détecter la fréquence dominante correspondante.
    La corrélation est calculée entre la forme d'onde et chaque fréquence cible, et la fréquence avec la corrélation maximale est détectée.
    Si la corrélation dépasse le seuil donné, la fréquence détectée est affichée, et si toutes les fréquences cibles sont détectées dans l'ordre,
    une alerte "HYPO" est déclenchée.

    Args:
        target (list): Liste des fréquences cibles à détecter.
        waveform (list): Forme d'onde à analyser sous forme de liste de valeurs d'amplitude.
        sample_format (int): Format d'échantillonage des valeurs d'amplitude.
        channels (int): Nombre de canaux audio.
        threshold (float): Seuil de corrélation pour la détection de fréquence.
        chunk_size (int): Taille de chaque chunk de la forme d'onde pour le calcul de corrélation.
        framerate (int): Taux d'échantillonnage de la forme d'onde.
    """

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
        if last_freq_Low_SG != max_freq:
            print(datetime.datetime.now().strftime("%H:%M:%S"), 'LOW_Info   : Fréquence détectée : {} Hz'.format(max_freq))
            detected_list_Low_SG.append(max_freq)
            last_freq_Low_SG = max_freq
            if len(detected_list_Low_SG) == len(target):
                if target == detected_list_Low_SG:
                    print(datetime.datetime.now().strftime("%H:%M:%S"),"\n\n              !!!!!!!!!!!! Alerte : HYPO !!!!!!!!!!!!       \n\n")
                    notification.alert("Alerte HYPO!", "Ok !", "./images/alerte_v2.png", "Une alerte HYPO a été détectée ...", "./alarmes/LOW.wav")
                    message = datetime.datetime.now().strftime("%H:%M:%S") + " ---------------- >  Alerte HYPO détectée < ---------------- "
                    logs.write_daily_log(message)

                detected_list_Low_SG = detected_list_Low_SG[1:]


def Alert_SG(target, waveform, sample_format,channels, threshold, chunk_size, framerate):
    """
    Effectue la détection des fréquences dans une forme d'onde donnée pour les signaux d'alerte.

    Cette fonction compare la forme d'onde donnée avec une liste de fréquences cibles pour détecter la fréquence dominante correspondante.
    La corrélation est calculée entre la forme d'onde et chaque fréquence cible, et la fréquence avec la corrélation maximale est détectée.
    Si la corrélation dépasse le seuil donné, la fréquence détectée est affichée, et si toutes les fréquences cibles sont détectées dans l'ordre,
    une alerte "URGENCE" est déclenchée.

    Args:
        target (list): Liste des fréquences cibles à détecter.
        waveform (list): Forme d'onde à analyser sous forme de liste de valeurs d'amplitude.
        sample_format (int): Format d'échantillonage des valeurs d'amplitude.
        channels (int): Nombre de canaux audio.
        threshold (float): Seuil de corrélation pour la détection de fréquence.
        chunk_size (int): Taille de chaque chunk de la forme d'onde pour le calcul de corrélation.
        framerate (int): Taux d'échantillonnage de la forme d'onde.
    """

    global detected_list_Alert_SG
    global last_freq_Alert_SG
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

        if last_freq_Alert_SG != max_freq:
            print(datetime.datetime.now().strftime("%H:%M:%S"), 'ALERT_Info : Fréquence détectée : {} Hz'.format(max_freq))
            detected_list_Alert_SG.append(max_freq)
            last_freq_Alert_SG = max_freq
            if len(detected_list_Alert_SG) == len(target):
                if target == detected_list_Alert_SG:
                    print(datetime.datetime.now().strftime("%H:%M:%S"),"\n\n              !!!!!!!!!!!! Alerte : URGENCE !!!!!!!!!!!!       \n\n")
                    notification.alert("Alerte URGENTE!", "Ok !", "./images/alerte_v2.png", "Une alerte URGENTE a été détectée ...", "./alarmes/ALERT.wav")
                    message = datetime.datetime.now().strftime("%H:%M:%S") + " ---------------- >  Alerte URGENTE détectée < ----------------  "
                    logs.write_daily_log(message)

                detected_list_Alert_SG = detected_list_Alert_SG[1:]


