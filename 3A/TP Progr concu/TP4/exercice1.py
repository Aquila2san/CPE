from multiprocessing import Process, Value, Semaphore
import random
import sys
import os
import time

def processus_p1(liste, N, somme, sem):
    somme_impairs = 0
    for i in range(1, N, 2):
        somme_impairs += liste[i]
    
    sem.acquire()  # Bloque l'accès à la variable partagée
    somme.value += somme_impairs
    time.sleep(0.01)
    sem.release()  # Libère l'accès

def processus_p2(liste, N, somme, sem):
    somme_pairs = 0
    for i in range(0, N, 2):
        somme_pairs += liste[i]
    
    sem.acquire()  # Bloque l'accès à la variable partagée
    somme.value += somme_pairs
    time.sleep(0.01)
    sem.release()  # Libère l'accès

# Initialisation
N = 100
ma_liste = [random.randint(1, 10) for _ in range(N)]
somme = Value('i', 0) 
sem = Semaphore(1)

# Création des processus
p1 = Process(target=processus_p1, args=(ma_liste, N, somme, sem))
p2 = Process(target=processus_p2, args=(ma_liste, N, somme, sem))

# Lancement
p1.start()
p2.start()

# Attente des résultats
p1.join()
p2.join()

print(f"Liste : {ma_liste}")
print(f"Somme : {somme.value}")