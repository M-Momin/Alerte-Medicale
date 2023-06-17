import wave
import struct
import math

# Paramètres du fichier WAV
nb_channels = 1
sample_width = 2
framerate = 44100
nb_frames = framerate * 5

# Liste des fréquences à générer
High_SG_frequencies = [1312, 1410, 1500, 1619, 1722]
Low_SG_frequencies = [1722, 1619, 1500, 1410, 1312]

# Fonction pour générer une onde sinusoïdale à une fréquence donnée
def generate_sine_wave(frequency, duration):
    """
    Génère une forme d'onde sinusoïdale.

    Cette fonction génère une forme d'onde sinusoïdale avec une fréquence donnée et une durée spécifiée.
    Elle utilise l'équation mathématique d'une sinusoïde pour calculer les échantillons de l'onde.

    Args:
        frequency (float): La fréquence de la sinusoïde en hertz.
        duration (float): La durée de la sinusoïde en secondes.
    """
    amplitude = 32767
    samples = []
    for i in range(int(duration * framerate)):
        sample = amplitude * math.sin(2 * math.pi * frequency * i / framerate)
        samples.append(struct.pack('h', int(sample)))
    return b''.join(samples)


# Création du fichier WAV
def wav_create():
    """
    Crée des fichiers audio WAV contenant des formes d'onde sinusoïdales.

    Cette fonction crée des fichiers audio WAV contenant des formes d'onde sinusoïdales pour des alarmes haute et basse.
    Les fréquences et les durées des sinusoïdes sont définies dans les listes `High_SG_frequencies` et `Low_SG_frequencies`.
    """

    with wave.open("High_SG_Alarm.wav", 'w') as wav_file:
        wav_file.setparams((nb_channels, sample_width, framerate, nb_frames, 'NONE', 'not compressed'))
        for i in range(5):
            for j in range(5):
                frequency = High_SG_frequencies[j]
                duration = 0.2
                sine_wave = generate_sine_wave(frequency, duration)
                wav_file.writeframes(sine_wave)
    with wave.open("Low_SG_Alarm.wav", 'w') as wav_file:
        wav_file.setparams((nb_channels, sample_width, framerate, nb_frames, 'NONE', 'not compressed'))
        for i in range(5):
            for j in range(5):
                frequency = Low_SG_frequencies[j]
                duration = 0.2
                sine_wave = generate_sine_wave(frequency, duration)
                wav_file.writeframes(sine_wave)

if __name__ == "__main__":
    wav_create()