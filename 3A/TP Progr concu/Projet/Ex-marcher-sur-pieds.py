# Mai 2023
# ex : on se marche sur les pieds

import multiprocessing as mp
import os

# Incrémentation sans protéger la variable partagée
def count1_on_se_marche_sur_les_pieds(nb_iterations):
    """ Chacun écrit à son rythme (non protégée)"""
    global variable_partagee
    for i in range(nb_iterations): 
        variable_partagee.value += 1
    
#----------- PARTIE principale (le point d'entrée de cet exemple -------
if __name__ == '__main__' :
    #Pour tenir compte du MacOS
    import os, platform
    if platform.system() == 'Windows':
        mp.set_start_method('spawn')
    else:
        mp.set_start_method('fork')
        
    nb_iterations = 10000
    # La variable partagée
    variable_partagee = mp.Value('i',0)  # ce sera un entier initialisé à 0
    
    # On crée 2 process
    id1=mp.Process(target= count1_on_se_marche_sur_les_pieds, args=(nb_iterations,))
    id2=mp.Process(target= count1_on_se_marche_sur_les_pieds, args=(nb_iterations,))
    id1.start(); id2.start()
 
    # Les fils ne reviennent plus ic    
    id1.join(); id2.join() 

    print("la valeur de variable_partagee APRES les incrémentations %d (attendu %d) "% (variable_partagee.value,nb_iterations*2))
"""
QQ traces
la valeur de variable_partagee APRES les incrémentations 10223 (attendu 20000) 
la valeur de variable_partagee APRES les incrémentations 10275 (attendu 20000) 
la valeur de variable_partagee APRES les incrémentations 10222 (attendu 20000) 
"""