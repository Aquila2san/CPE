from multiprocessing import Process, Semaphore
import time

# Définition des tâches
def tache_A(sem_A):
    print("Tâche A : Début")
    time.sleep(0.5)
    print("Tâche A : Fin")
    # Libère B, C et D
    sem_A.release()
    sem_A.release()
    sem_A.release()

def tache_B(sem_A, sem_BC):
    sem_A.acquire()  # Attend A
    print("Tâche B : Début")
    time.sleep(0.5)
    print("Tâche B : Fin")
    sem_BC.release()  # Signal pour E

def tache_C(sem_A, sem_BC):
    sem_A.acquire()  # Attend A
    print("Tâche C : Début")
    time.sleep(0.5)
    print("Tâche C : Fin")
    sem_BC.release()  # Signal pour E

def tache_D(sem_A, sem_DE):
    sem_A.acquire()  # Attend A
    print("Tâche D : Début")
    time.sleep(0.5)
    print("Tâche D : Fin")
    sem_DE.release()  # Signal pour F

def tache_E(sem_BC, sem_DE):
    sem_BC.acquire()  # Attend B
    sem_BC.acquire()  # Attend C
    print("Tâche E : Début")
    time.sleep(0.5)
    print("Tâche E : Fin")
    sem_DE.release()  # Signal pour F

def tache_F(sem_DE):
    sem_DE.acquire()  # Attend D
    sem_DE.acquire()  # Attend E
    print("Tâche F : Début")
    time.sleep(0.5)
    print("Tâche F : Fin")

# Initialisation des sémaphores à 0 (bloquants par défaut)
sem_A = Semaphore(0)
sem_BC = Semaphore(0)
sem_DE = Semaphore(0)

# Création des processus
pA = Process(target=tache_A, args=(sem_A,))
pB = Process(target=tache_B, args=(sem_A, sem_BC))
pC = Process(target=tache_C, args=(sem_A, sem_BC))
pD = Process(target=tache_D, args=(sem_A, sem_DE))
pE = Process(target=tache_E, args=(sem_BC, sem_DE))
pF = Process(target=tache_F, args=(sem_DE,))

# Lancement des processus (ils démarrent tous en même temps, mais se bloquent via les sémaphores)
pA.start()
pB.start()
pC.start()
pD.start()
pE.start()
pF.start()

# Attente du processus final
pF.join()
print("Toutes les tâches sont terminées.")