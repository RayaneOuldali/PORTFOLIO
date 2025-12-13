# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 09:01:08 2025

@author: Admin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Charge le CSV
dataframe = pd.read_csv("server_usage_data.csv")

dataset = dataframe.to_numpy()
#print(dataset)
CPU_usage= np.array([])
Memory_usage = np.array([])
Network_usage = np.array([])
Temperature = np.array([])
date = np.array([])


#Recupe chaque element de ligne et les range dans un tableau numpy
for dataliste in dataset:
    CPU_usage = np.append(CPU_usage,dataliste[1])
    Memory_usage = np.append(Memory_usage, dataliste[2])
    Network_usage = np.append(Network_usage, dataliste[3])
    Temperature = np.append(Temperature, dataliste[-1])
    date = np.append(date, dataliste[0])
    
    #print(dataliste[1],"CPU Usage")

def moyenne(tab):
    return tab.mean()

def EcartType(tab):
    return tab.std()

def Variance(tab):
    return tab.var()

def MaxMin(tab):
    return [tab.min(),tab.max()]


def figure2d(TempsX,TabY,TitreGraphique):
    plt.plot(TempsX,TabY)
    plt.title(TitreGraphique)  # titre
    plt.xlabel("X")       # label axe X
    plt.ylabel("Y")       # label axe Y
    plt.grid(True)        # grille
    plt.show()            # affiche le graphique
    


#Affichage des resultat
print("===============Affichage stat basique===============")
print("===============Moyenne===============")
print(moyenne(CPU_usage),"CPU Usage")
print(moyenne(Memory_usage),"Memory Usage")
print(moyenne(Network_usage),"Network Usage")
print(moyenne(Temperature),"Temperature")
print("===============Ecart Type===============")
print(EcartType(CPU_usage),"CPU Usage")
print(EcartType(Memory_usage),"Memory Usage")
print(EcartType(Network_usage),"Network Usage")
print(EcartType(Temperature),"Temperature")
print("===============Variance===============")
print(Variance(CPU_usage),"CPU Usage")
print(Variance(Memory_usage),"Memory Usage")
print(Variance(Network_usage),"Network Usage")
print(Variance(Temperature),"Temperature")
print("===============Max Min===============")
print(MaxMin(CPU_usage),"CPU Usage")
print(MaxMin(Memory_usage),"Memory Usage")
print(MaxMin(Network_usage),"Network Usage")
print(MaxMin(Temperature),"Temperature")
print("=====================================")

print(figure2d(date, CPU_usage, "CPU Usage"))
print(figure2d(date, Memory_usage, "Memory Usage"))
print(figure2d(date, Network_usage, "Network Usage"))
print(figure2d(date, Temperature, "Temperature"))



