import sounddevice as sd
import numpy as np

###Creation fonction### 

def encode_manchester(binary):
    manchester = ''
    for bit in binary:
        if bit == '1':
            manchester += '01'
        elif bit == '0':
            manchester += '10'
        else:
            return 'Erreur: le nombre binaire contient des caractères invalides.'
    return manchester


###Ecriture du message###


bits = ''
binaire = ""
zero = 0
un = 0
liste = []
donner =[]

message = input("écrivez votre message de 10 lettres max:")

while len(message)>10:
    
    message = input("écrivez votre message de 10 lettres max:")

    
###Passage en décimal ASCII###


l = len(message)
for i in range(l):
    liste.append(ord(message[i]))
    
print("Code ascii : ", liste)


###Passage en binaire###


for j in range(l):
    liste[j] = bin(liste[j])[2:]
    
print("Code binaire : ", liste)


###Ajout bit de parité###


for n in range(l):
    if len(liste[n])==6:
        liste[n]="0"+liste[n]
for ele in range(l):
    char_bin=liste[ele]
    for c in range(len(char_bin)):
        if char_bin[c]=="0":
            zero=zero+1
        else:
            un=un+1
    if un%2==0:
        liste[ele]="0"+liste[ele]
    else:
        liste[ele]="1"+liste[ele]
    zero=0
    un=0
    
print("Code binaire avec bit de parité :", liste)

binaire = ''.join(liste)
binary_number = binaire
codem = encode_manchester(binary_number)

print("manchester :", codem)


###emission du signal###


for bit in codem:
    donner.append(bit)
for elt in donner:
        for elt2 in range(len(elt)):
            #print(elt[elt2],"liste élément")
            if elt[elt2]=='1':
                duration = 2
                sample_rate = 44100
                frequency = 6000
                t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
                la_note = 0.5 * np.sin(2 * np.pi * frequency * t)
                sd.play(la_note, sample_rate)
                sd.wait()
            elif elt[elt2]=='0':
                duration = 2
                sample_rate = 44100
                frequency = 4000
                t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
                la_note = 0.5 * np.sin(2 * np.pi * frequency * t)
                sd.play(la_note, sample_rate)
                sd.wait()
