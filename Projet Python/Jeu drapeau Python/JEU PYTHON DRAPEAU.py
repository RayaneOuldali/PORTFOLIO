# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 11:59:40 2024

@author: Admin
"""
import tkinter as tk
from PIL import ImageTk, Image
    
    
    #definition des fonction pour changer de page 
def vers_jeu():
    accueil.pack_forget()
    jeu.pack()
        
        
    #Fonction appelée lorsqu'on clique sur le bouton
def afficher_jeu(l_pays,pays_image):
    compteur = 0
    valeur = champ_saisie.get()  # Récupérer la valeur saisie dans le champ
    print("La valeur saisie est:", valeur)
    for chemin in pays_image:
        image = Image.open(chemin)
        photo = ImageTk.PhotoImage(image)
        label.configure(image=photo)
        label.image = photo
        if valeur.lower() in l_pays:
            compteur+=1
# def afficher_jeu(l_pays, pays_image):
#     valeur = champ_saisie.get().lower()  # Récupérer la valeur saisie dans le champ et convertir en minuscules
#     print("La valeur saisie est:", valeur)
#     for i, pays in enumerate(l_pays):
#         print(i)
#     #     if valeur in pays.lower():
#     #         image_path = pays_image[i]  # Obtenez le chemin de l'image correspondante
#     #         image = Image.open(image_path)
#     #         photo = ImageTk.PhotoImage(image)
#     #         label.configure(image=photo)
#     #         label.image = photo
#     #         break  # Sortez de la boucle dès que vous trouvez une correspondance
#     # else:
#     #     # Si aucun pays ne correspond, vous pouvez afficher un message ou une image par défaut
#     #     print("Aucun pays ne correspond à la saisie")

    
        
  
base = tk.Tk()
base.title("gues the flag")
    
    
accueil = tk.Frame(base)#C'est quoi Frame

bouton_accueil = tk.Button(accueil, text="Jouer", command=vers_jeu)
bouton_accueil.pack()
    
accueil.pack()
    
jeu = tk.Frame(base)
    
    # Charger l'image avec PIL ### ici on remplacera par les image qui sont dans la liste 
image_path = r"C:\Users\Admin\Documents\Projet perso\Guess the flag\ALLEMAGNE.PNG"  # Remplacez par le chemin de votre première image
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)
    
    # Créer un widget Label pour afficher l'image
label = tk.Label(jeu, image=photo)
label.pack()
    
    # Création du champ de saisie
champ_saisie = tk.Entry(jeu, width=30)  # Largeur du champ en caractères
champ_saisie.pack(pady=10)  # Espacement autour du champ
    


def cree_dico_pays():
# Listage de tout les drapeaux d'europe
    ALLEMAGNE = r"C:\Users\Admin\Documents\Projet perso\Guess the flag\ALLEMAGNE.PNG"
    AUTRICHE = r"C:\Users\Admin\Documents\Projet perso\Guess the flag\AUTRICHE.PNG"
    BELGIQUE = r"C:\Users\Admin\Documents\Projet perso\Guess the flag\BELGIQUE.PNG"


    Dico_pays = {ALLEMAGNE:'Allemagne',AUTRICHE:'Autriche',BELGIQUE:'Belgique'}
    return Dico_pays


def lPays(Dico_pays):
    #Recupere la valeur du pays 
    liste_pays = Dico_pays.values()
    print(liste_pays)
    return liste_pays

def pays_image(Dico_pays):
    #recupere l'emplacement de l'image sur mon pc (sous forme de liste)
    pays_image_liste = Dico_pays.keys()
    return pays_image_liste
    
       
        
        
dico_pays_eu = cree_dico_pays()
liste_pays=lPays(dico_pays_eu)
pays_image = pays_image(dico_pays_eu)

print(jeu(pays_image,liste_pays))
    
    
    # Création du bouton
bouton = tk.Button(jeu, text="Valider", command=afficher_jeu(liste_pays,pays_image))
bouton.pack()
    
    # Exécuter la boucle principale de l'application
base.mainloop()
