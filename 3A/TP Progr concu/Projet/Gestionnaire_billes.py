# =============================================================================
# CODE COMPLET : GESTIONNAIRE DE BILLES
# =============================================================================

import multiprocessing as mp
import time
import random
import ctypes

def demander(k_billes, nbr_disponible_billes, verrou, condition_billes):
    with verrou: #
        while nbr_disponible_billes.value < k_billes:
            condition_billes.wait() # Relâche le verrou
        
        # Le processus est réveillé
        nbr_disponible_billes.value -= k_billes
        print(f"[Travailleur {mp.current_process().name}] Réquisition de {k_billes} billes. Reste: {nbr_disponible_billes.value}")
        
def rendre(k_billes, nbr_disponible_billes, verrou, condition_billes):
    with verrou: 
        nbr_disponible_billes.value += k_billes
        print(f"[Travailleur {mp.current_process().name}] Restitution de {k_billes} billes. Reste: {nbr_disponible_billes.value}")
        
        # Réveille TOUS les processus endormis
        condition_billes.notify_all()
        
def travailleur(k_billes, nbr_disponible_billes, verrou, condition_billes, m_iterations):
    for i in range(m_iterations):
        time.sleep(random.uniform(0.1, 0.5)) # Temps d'attente aléatoire avant de demander
        
        demander(k_billes, nbr_disponible_billes, verrou, condition_billes) # Bloquant si pas assez de billes
        
        time.sleep(k_billes * 0.1) # Simule l'utilisation des ressources (le travail)
        
        rendre(k_billes, nbr_disponible_billes, verrou, condition_billes)
        
def controleur(nbr_disponible_billes, max_billes, verrou, keep_running):
    while keep_running.value:
        time.sleep(0.5) # Fréquence de contrôle
        with verrou:
            valeur_actuelle = nbr_disponible_billes.value
            # Vérification stricte des bornes de la ressource
            if not (0 <= valeur_actuelle <= max_billes):
                print(f"[CONTRÔLEUR] ALERTE INCOHÉRENCE : Stock de billes anormal ({valeur_actuelle}) !")
        
if __name__ == "__main__":
    NB_MAX_BILLES = 9
    nbr_billes_partagees = mp.Value('i', NB_MAX_BILLES) # Variable entière partagée
    
    # Création du verrou et liaison obligatoire avec la Condition
    verrou_partage = mp.Lock()
    condition_billes = mp.Condition(verrou_partage)
    
    keep_running_controleur = mp.Value(ctypes.c_bool, True)
    
    # Définition des demandes des 4 processus selon l'énoncé : (4, 3, 5, 2)
    demandes_billes = [4, 3, 5, 2]
    processus_travailleurs = []
    
    # Lancement du contrôleur
    p_ctrl = mp.Process(target=controleur, args=(nbr_billes_partagees, NB_MAX_BILLES, verrou_partage, keep_running_controleur))
    p_ctrl.start()
    
    # Lancement des 4 travailleurs
    for idx, k in enumerate(demandes_billes):
        p = mp.Process(target=travailleur, name=f"P{idx+1}", args=(k, nbr_billes_partagees, verrou_partage, condition_billes, 3))
        processus_travailleurs.append(p)
        p.start()
        
    # Attente de la fin des travailleurs
    for p in processus_travailleurs:
        p.join()
        
    # Arrêt du contrôleur devenu inutile
    keep_running_controleur.value = False
    p_ctrl.join()
    print("Tous les travailleurs ont fini. Système arrêté proprement.")
        