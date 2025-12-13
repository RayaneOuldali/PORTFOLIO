import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import matplotlib.pyplot as plt
import numpy as np
import librosa

def regrouper_par_8(codebp_recu):

    # Crée une liste de listes, chaque sous-liste contenant 8 éléments
    octet = [codebp_recu[i:i+8] for i in range(0, len(codebp_recu), 8)]

    # Concatène les éléments de chaque groupe
    octetbp_recu = [''.join(map(str, groupe)) for groupe in octet]

    return octetbp_recu

def detect_binary_sequence(file_path, freq_range_0, freq_range_1, threshold=0.5, duration_threshold=1):
    # Charger le fichier audio WAV
    signal, sr = librosa.load(file_path, sr=None)

    # Calculer la transformée de Fourier
    stft = librosa.stft(signal)
    frequencies = librosa.fft_frequencies(sr=sr)
    magnitudes = np.abs(stft)

    # Définir les indices des fréquences dans les plages spécifiées
    indices_0 = np.where((frequencies >= freq_range_0[0]) & (frequencies <= freq_range_0[1]))[0]
    indices_1 = np.where((frequencies >= freq_range_1[0]) & (frequencies <= freq_range_1[1]))[0]

    # Détecter les moments où l'un des pics de fréquence est dominante
    binary_sequence = []
    current_duration = 0

    for mag in magnitudes.T:
        # Trouver les indices des pics dans chaque plage de fréquences
        peaks_0 = np.where(mag[indices_0] > threshold * np.max(mag))[0]
        peaks_1 = np.where(mag[indices_1] > threshold * np.max(mag))[0]

        # Attribuer 0 ou 1 en fonction des pics détectés
        if len(peaks_0) > 0:
            binary_sequence.append(0)
            current_duration += 1
        elif len(peaks_1) > 0:
            binary_sequence.append(1)
            current_duration += 1
        else:
            binary_sequence.append(None)
            current_duration = 0

        # Vérifier si la durée minimale est atteinte
        if current_duration >= duration_threshold:
            # Réinitialiser la durée après avoir attribué le 0 ou le 1
            current_duration = 0

    # Vérifier que le spectrogramme n'est pas vide avant d'essayer de l'afficher
    if magnitudes.size > 0:
        # Afficher le spectrogramme
        plt.figure(figsize=(12, 6))
        plt.imshow(librosa.amplitude_to_db(magnitudes, ref=np.max), cmap='viridis', aspect='auto', origin='lower')
        plt.title('Spectrogramme')
        plt.xlabel('Temps')
        plt.ylabel('Fréquence')
        plt.colorbar(format='%+2.0f dB')
        plt.show()

    return binary_sequence

def manchester_decode(codem_recu):
    codebp_recu = []

    # La longueur de la séquence binaire
    length = len(codem_recu)

    # Parcours de la séquence binaire
    for i in range(0, length, 2):
        # Si la paire est '01', ajouter 1 à la séquence décodée
        if codem_recu[i] == 0 and codem_recu[i + 1] == 1:
            codebp_recu.append(1)
        # Si la paire est '10', ajouter 0 à la séquence décodée
        elif codem_recu[i] == 1 and codem_recu[i + 1] == 0:
            codebp_recu.append(0)
        else:
            # Gérer une erreur si la séquence n'est pas valide
            raise ValueError("La séquence binaire n'est pas compatible avec le codage Manchester.")

    return codebp_recu

def detecter_erreur(codebp_recu):
    for caractere in codebp_recu:
        bit_de_parite = int(caractere[0])
        donnees = caractere[1:]

        # Vérifier la parité
        if (donnees.count('1') % 2 == 0 and bit_de_parite == 1) or \
           (donnees.count('1') % 2 == 1 and bit_de_parite == 0):
            print(f"Erreur détectée dans le caractère {caractere}")
        else:
            print(f"Aucune erreur détectée dans le caractère {caractere}")


###reception et enregistrement###


freq = 44100


duration =320

recording = sd.rec(int(duration * freq), 
                   samplerate=freq, channels=2)

sd.wait()

write("Help.wav", freq, recording)

wv.write("Help.wav", recording, freq, sampwidth=2)


###analyse du signal###



# Appeler la fonction avec le chemin de votre fichier audio et les plages de fréquences spécifiques
audio_file_path = 'help.wav'
freq_range_0 = (15950, 16050)  # Plage de fréquences pour représenter le 0
freq_range_1 = (17950, 18050)  # Plage de fréquences pour représenter le 1
result_sequence = detect_binary_sequence(audio_file_path, freq_range_0, freq_range_1)

print("Séquence binaire détectée :", result_sequence)


###réception du manchester###

n=-1
ni = 0
codem_recu = []

for i in range(1, len(result_sequence)): 
    if(n == result_sequence[i]):     
        ni = ni+1      
    else:
        if(ni >= 15 and result_sequence[i-1] != None):
            codem_recu.append(result_sequence[i-1])
        ni = 0
    n = result_sequence[i]

codem_recu=[1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1]
print("Code en Manchester", codem_recu)


###récupération du binaire###


codebp_recu = manchester_decode(codem_recu)

print("Code sans le Manchester : ", codebp_recu)


###Regroupement en octet###


octetbp_recu = regrouper_par_8(codebp_recu)

# Affiche les groupes concaténés
for groupe_concatene in octetbp_recu:
    print(groupe_concatene)
# Stocke les groupes d'octets dans une liste

codebp_recu = octetbp_recu

print("Code binaire en octet :", codebp_recu)


###retrait du bit de parité et retour si une erreur a été commise###


detecter_erreur(codebp_recu)


###Supprimer le bit de parité###


codeb_recu = [codebp_recu[1:] for codebp_recu in codebp_recu]

print("Code binaire : ",codeb_recu)


###récupération de l'ASCII###


ascii_list = []

# Boucle pour chaque élément binaire dans la liste
for binary_code in codeb_recu:
    # Convertit le code binaire en caractère ASCII
    ascii_char = chr(int(binary_code, 2))
    
    # Ajoute le caractère ASCII à la liste
    ascii_list.append(ascii_char)

# Affiche la liste des caractères ASCII
print("Caractères ASCII correspondants :", ', '.join(ascii_list))
