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
    # Calcul de la corrélation entre la forme d'onde et chaque fréquence cible
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
    # Calcul de la corrélation entre la forme d'onde et chaque fréquence cible
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
                    notification.alert("Alerte URGENTE!", "Ok !", "./images/alerte_v2.png", "Une alerte URGENTE a été détectée ...")
                    message = datetime.datetime.now().strftime("%H:%M:%S") + " ---------------- >  Alerte URGENTE détectée < ----------------  "
                    logs.write_daily_log(message)

                detected_list_Alert_SG = detected_list_Alert_SG[1:]


