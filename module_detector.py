import pyaudio
import numpy as np
from scipy.io import wavfile
from scipy.signal import correlate, find_peaks

# Charger le fichier WAV
rate, wav_data = wavfile.read("Low.wav")

# Extraire les fréquences et leurs amplitudes
freqs, amps = np.fft.fftfreq(len(wav_data)), np.fft.fft(wav_data)

# Trouver les pics de fréquences
peak_indices, _ = find_peaks(np.abs(amps.real), height=1000, distance=10)

# Trier les pics par ordre de fréquence
peak_frequencies = freqs[peak_indices]
peak_order = np.argsort(peak_frequencies)

# Paramètres d'enregistrement
chunk_size = 1024
sample_format = pyaudio.paInt16
channels = 1
rate = 44100

# Initialiser PyAudio
p = pyaudio.PyAudio()

# Ouvrir le flux audio
stream = p.open(format=sample_format,
                channels=channels,
                rate=rate,
                frames_per_buffer=chunk_size,
                input=True)

print("Enregistrement en cours...")

# Boucle d'enregistrement
while True:
    # Lire un échantillon du flux audio
    data = stream.read(chunk_size)
    
    # Convertir les données en un tableau NumPy
    samples = np.frombuffer(data, dtype=np.int16)
    
    # Effectuer la transformée de Fourier discrète sur les échantillons
    fft = np.fft.fft(samples)
    
    # Trouver les pics de fréquences
    peak_indices, _ = find_peaks(np.abs(fft.real), height=1000, distance=10)
    
    # Trier les pics par ordre de fréquence
    peak_frequencies = freqs[peak_indices]
    peak_order = np.argsort(peak_frequencies)
    
    # Vérifier si les pics de fréquences correspondent à ceux du fichier WAV
    if np.allclose(peak_frequencies[peak_order], freqs[peak_indices][peak_order], rtol=1e-3):
        print("Signal détecté !")
