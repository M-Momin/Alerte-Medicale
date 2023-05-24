import wave
import struct
import math

# Paramètres du fichier WAV
framerate = 44100
num_samples = framerate * 2
amplitude = 32767.0
num_channels = 1
sample_width = 2

# Liste des fréquences à générer
High_SG_frequencies = [1312, 1410, 1500, 1619, 1722]
Low_SG_frequencies = [1722, 1619,1500,1410,1312]
# Création du fichier WAV
with wave.open('High_SG_frequencies.wav', 'w') as wavfile:
    wavfile.setparams((num_channels, sample_width, framerate, num_samples, 'NONE', 'not compressed'))
    for freq in High_SG_frequencies:
        # Génération de la forme d'onde sinusoïdale
        waveform = []
        for i in range(num_samples):
            t = float(i) / float(framerate)
            value = int(amplitude * math.sin(2.0 * math.pi * freq * t))
            waveform.append(value)
        # Conversion de la forme d'onde en format binaire
        binary_waveform = struct.pack('h' * num_samples, *waveform)
        # Écriture de la forme d'onde dans le fichier WAV
        wavfile.writeframes(binary_waveform)
with wave.open('Low_SG_frequencies.wav', 'w') as wavfile:
    wavfile.setparams((num_channels, sample_width, framerate, num_samples, 'NONE', 'not compressed'))
    for freq in Low_SG_frequencies:
        # Génération de la forme d'onde sinusoïdale
        waveform = []
        for i in range(num_samples):
            t = float(i) / float(framerate)
            value = int(amplitude * math.sin(2.0 * math.pi * freq * t))
            waveform.append(value)
        # Conversion de la forme d'onde en format binaire
        binary_waveform = struct.pack('h' * num_samples, *waveform)
        # Écriture de la forme d'onde dans le fichier WAV
        wavfile.writeframes(binary_waveform)

