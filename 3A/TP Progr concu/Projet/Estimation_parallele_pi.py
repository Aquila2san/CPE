# =============================================================================
# CODE COMPLET : ESTIMATION PARALLÈLE DE PI (MONTE-CARLO)
# =============================================================================

import random
import time
import multiprocessing as mp

# Fonction exécutée par chaque processus travailleur
def frequence_de_hits_pour_n_essais(nb_iteration, queue_resultat):
    count = 0
    random.seed()
    
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
        # Si le point est dans le quart de cercle unitaire
        if x*x + y*y <= 1: 
            count += 1
            
    # Envoi du sous-total local au processus père via la Queue
    queue_resultat.put(count)

# La partie principale :
if __name__ == "__main__":
    import platform
    if platform.system() == "Darwin":
        mp.set_start_method('fork')

    N = 10000000          # Nombre total d'essais pour l'estimation
    nb_processus = 4      # Nombre de processus (k)
    iterations_par_processus = N // nb_processus

    # Structure de communication pour centraliser les résultats
    queue_res = mp.Queue()
    mes_process = []

    print(f"Lancement du calcul parallèle avec {nb_processus} processus...")
    print(f"Chaque processus va effectuer {iterations_par_processus} itérations.")
    
    # Début de la mesure du temps global
    start_time = time.time()

    # Création et démarrage des k processus
    for i in range(nb_processus):
        p = mp.Process(target=frequence_de_hits_pour_n_essais, args=(iterations_par_processus, queue_res))
        mes_process.append(p)
        p.start()

    # Collecte des résultats depuis la Queue
    total_hits = 0
    for i in range(nb_processus):
        total_hits += queue_res.get()

    # Attente de la fin de tous les processus
    for p in mes_process:
        p.join()

    # Fin de la mesure du temps
    end_time = time.time()

    # Calcul final de la valeur de Pi et affichage
    pi_estime = 4 * total_hits / N
    print("\n" + "="*50)
    print(f"Valeur estimée Pi par la méthode Multi-Processus : {pi_estime}")
    print(f"Temps de calcul total : {end_time - start_time:.4f} secondes")
    print("="*50)