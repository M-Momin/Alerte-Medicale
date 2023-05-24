import pyaudio
import numpy as np

# Paramètres de l'enregistrement
CHUNK_SIZE = 1024  # taille des chunks pour l'enregistrement
FORMAT = pyaudio.paInt16  # format audio
CHANNELS = 1  # nombre de canaux audio (1=mono, 2=stéréo)
RATE = 44100  # taux d'échantillonnage en Hz
DURATION = 0.2  # durée de chaque note en secondes
TARGET_FREQS = [1312, 1410, 1500, 1619, 1722]  # fréquences cibles
TARGET_SIZE = len(TARGET_FREQS)  # taille de la série de fréquences cibles
TARGET_AMPLITUDE = 10000  # seuil d'amplitude pour la corrélation

# Fonction pour détecter la série de fréquences cibles
def detect_sequence(data):
    freq_domain = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(len(data), d=1/RATE)
    amplitudes = np.abs(freq_domain)

    # Recherche de la série de fréquences cible
    corr = np.zeros(len(data) - TARGET_SIZE + 1)
    for i in range(len(corr)):
        corr[i] = np.sum(np.abs(freq_domain[i:i+TARGET_SIZE] - TARGET_AMPLITUDE)) / TARGET_SIZE

    corr_indices = np.argsort(corr)[:10]  # les 10 meilleurs correspondances
    corr_values = corr[corr_indices]

    # Vérification de la série de fréquences cible
    for i, index in enumerate(corr_indices):
        if corr_values[i] < TARGET_AMPLITUDE * TARGET_SIZE:
            break  # seuil d'amplitude pour la corrélation atteint
        if np.allclose(freqs[index:index+TARGET_SIZE], TARGET_FREQS, rtol=0.1):
            print("Série de fréquences cible détectée en ordre croissant !")
            return True  # retourne True si la série de notes est détectée en ordre croissant

    return False  # retourne False si la série de notes n'est pas détectée en ordre croissant

# Initialisation de PyAudio
pa = pyaudio.PyAudio()
stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

# Boucle d'enregistrement
try:
    while True:
        # Enregistrement de la série de notes
        data = np.zeros(int(RATE * DURATION * TARGET_SIZE))
        for i in range(TARGET_SIZE):
            data[i*int(RATE*DURATION):(i+1)*int(RATE*DURATION)] = np.frombuffer(stream.read(int(RATE*DURATION*CHUNK_SIZE)), dtype=np.int16)

        # Vérification de la série de notes
        if detect_sequence(data):
            print("Appuyez sur Enter pour continuer...")
            input()
except KeyboardInterrupt:
    pass

# Fermeture de PyAudio
stream.stop_stream()
stream.close()
pa.terminate()