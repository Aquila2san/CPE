############################################################################################################################################
# Objectif : Réaliser des programmes pour le TP 3
# Date : 29 septembre 2025
# Auteur : Victor Saunier
# ToDo : 
############################################################################################################################################

import random as rd

def ouvrir_fichier():
    '''Fonction permettant d'ouvrir le fichier mots.txt contenant des mots et de convertir ce fichier 
    en une liste python. Cette fonction renvoie la liste des most contenu dans le fichier'''
    with open("mots.txt", "r") as fichier:
        mots = fichier.read()
        liste_mots = mots.split()
        return (liste_mots)

def pendu_simple():
    '''Fonction realisant le jeu du pendu. Cette fonction demande à l'utilisateur de donner des lettres
    et lui laisse 8 chances pour trouver le mot. Cette fonction renvoie soit que l'utilisateur a trouvé
    le mot soit qu'il ne l'a pas trouvé et lui donne alors le mot'''
    liste_mots = ouvrir_fichier()
    mot = liste_mots[rd.randint(0, len(liste_mots)-1)] # Choix aléatoire du mot
    lettres_trouvees = [mot[0]] + ["_"] * (len(mot) - 1)
    nb_chances = 8
    while nb_chances > 0 and "_" in lettres_trouvees:
        print (lettres_trouvees)
        lettre = input("Quelle lettre choisissez vous ?")
        if lettre in mot:
            for k in range(len(mot)): # Parcours des lettres du mot pour trouver la position de la lettre trouvée
                if lettre == mot[k]:
                    lettres_trouvees[k] = lettre
        else:
            nb_chances -= 1
    if "_" in lettres_trouvees:
        print ("Dommage vous avez perdu ! Le mot était :", mot)
    else : 
        print ("Félécitations vous avez gagné ! Le mot est bien : ", mot)


def pendu_v2():
    '''Fonction realisant le jeu du pendu. Cette fonction demande à l'utilisateur de donner des lettres
    et lui laisse 8 chances pour trouver le mot. Cette fonction renvoie soit que l'utilisateur a trouvé
    le mot soit qu'il ne l'a pas trouvé et lui donne alors le mot. De plus cette fonction indique à 
    l'utilisateur si il réutilise une lettre qu'il a déja donné, lui propose de rejouer a la fin et 
    retiens le meilleur score des parties déja jouées'''
    liste_mots = ouvrir_fichier()
    mot = liste_mots[rd.randint(0, len(liste_mots)-1)] # Choix aléatoire du mot
    lettres_trouvees = [mot[0]] + ["_"] * (len(mot) - 1)
    lettres_donnees = []
    nb_chances = 8
    meilleur_score = 0
    while nb_chances > 0 and "_" in lettres_trouvees: # Boucle s'arrêtant quand l'utilisateur a utilisé ses 8 chances ou quand il a trouvé toutes les lettres
        print (lettres_trouvees)
        lettre = input("Quelle lettre choisissez vous ?")
        if lettre in lettres_donnees:
            nb_chances -= 1
            print ("Vous avez déjà donné cette lettre")
        else:
            lettres_donnees.append(lettre)
            if lettre in mot:
                for k in range(len(mot)): # Parcours des lettres du mot pour trouver la position de la lettre trouvée
                    if lettre == mot[k]:
                        lettres_trouvees[k] = lettre
            else:
                nb_chances -= 1
    if "_" in lettres_trouvees:
        print ("Dommage vous avez perdu ! Le mot était :", mot)
    else : 
        print ("Félécitations vous avez gagné ! Le mot est bien : ", mot)
    if nb_chances > meilleur_score: 
        meilleur_score = nb_chances # Changement du meilleur score qui correspond au nombre de chances restantes à la fin du pendu
    print ("Votre meilleur score est :", meilleur_score)
    choix = input("Voulez-vous rejouer ? (o/n)") # Proposition de rejouer à l'utilisateur
    if choix == "o" :
        pendu_v2()

from tkinter import *

print (pendu_v2())

    