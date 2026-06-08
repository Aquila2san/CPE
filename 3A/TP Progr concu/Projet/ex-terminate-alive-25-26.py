# Mai 2026 : révision, je renomme les fonc et mets plus de trace.
# MAi 26 : ATTENTION : une fois "set_method utilisé" (peut être même pas utilisé dans main, eg pour LES MAC comme ici), 
# **** on ne peut pas appeler "set_method". Fera une exception "already set".
# La seule facon d'utiliser  spawn dans une fonction est d'utiliser 
# cntx = multiprocessing.get_context('spawn')
# Puis de créer les processus via cet env de spawn obtenu.
# p = cntx.Process(target=time.sleep, args=(1000,))
# ATTENTION : si on demandait dans ce cas quel est la "method" utilisé, on aura "fork" (via get_start_method())
#          mais les processus seront créés par la methode spawn (se voit dans les traces).

# Crée en 2024-25 ?
import multiprocessing, time, signal

def multiprocessing_FORK_alive_terminate() :
    print("Exemples avec fork (par défaut linux, sous MAC, il faut le demander)")
    
    # multiprocessing.set_start_method('fork') : Err : already set ! Même si je l'enlève de main !!!
    
    print(f"Quele est le méthode de création de Processs : {multiprocessing.get_start_method()}")
    # Quele est le méthode de création de Processs : fork
    
    p = multiprocessing.Process(target=time.sleep, args=(1000,))
    print("is_alive : ",p, p.is_alive())
    #<...Process ... initial> False
    p.start()
    print("is_alive : ",p, p.is_alive())
    #<...Process ... started> True
    print("terminate : ", p.terminate())
    time.sleep(0.1)
    print("is_alive : ", p, p.is_alive())
    #<...Process ... stopped exitcode=-SIGTERM> False
    print(p.exitcode == -signal.SIGTERM)
 
"""
Quele est le méthode de création de Processs : fork
================================================================================    
Exemples avec fork (par défaut sous linux, sous MAC, il faut le demander)
Quele est le méthode de création de Processs : spawn
is_alive :  <Process name='Process-1' parent=52251 initial> False
is_alive :  <Process name='Process-1' pid=52253 parent=52251 started> True
terminate :  None
is_alive :  <Process name='Process-1' pid=52253 parent=52251 stopped exitcode=-SIGTERM> False
True
"""
    
# Pour passer à "spawn" seul marche "get_context('spawn')" suivi de création via le contexte de spawn obtenu
# Pas de set_method ni set_context (qui n'existe pas !)
def multiprocessing_SPAWN_alive_terminate() : # 2e
    print("Exemples avec spawn (linux, MAC, PC ?)")
    print(f"Quele est le méthode de création de Processs : {multiprocessing.get_start_method()}")
    # Quele est le méthode de création de Processs : fork
        
    
    # multiprocessing.set_start_method('spawn')
    # Err : RuntimeError: context has already been set
    
    # Fait Erreur : pas de méthode set_context (get oui mais pas set)
    # mp_context = multiprocessing.set_context('spawn') 


    mp_context = multiprocessing.get_context('spawn')

    
    print(f"Quele est le méthode de création de Processs : {multiprocessing.get_start_method()}")
    # Quele est le méthode de création de Processs : fork
    # Mais les messages suivants montrent que les process sont créés avec Spawn
    
    p = mp_context.Process(target=time.sleep, args=(1000,))
    print("is_alive : ",p, p.is_alive())
    #<...Process ... initial> False
    p.start()
    print("is_alive : ",p, p.is_alive())
    #<...Process ... started> True
    print("terminate : ", p.terminate())
    time.sleep(0.1)
    print("is_alive : ", p, p.is_alive())
    #<...Process ... stopped exitcode=-SIGTERM> False
    print(p.exitcode == -signal.SIGTERM)
"""
Exemples avec spawn (linux)
Quele est le méthode de création de Processs : fork
Quele est le méthode de création de Processs : fork
is_alive :  <SpawnProcess name='SpawnProcess-2' parent=51383 initial> False
is_alive :  <SpawnProcess name='SpawnProcess-2' pid=51386 parent=51383 started> True
terminate :  None
is_alive :  <SpawnProcess name='SpawnProcess-2' pid=51386 parent=51383 stopped exitcode=-SIGTERM> False
True

"""  
    
    
# A propos de Process.close()
"""
Ferme l'objet Process, libérant  toutes les ressources qui lui sont associées. 
ATTENTION : Une exception ValueError est levée si le processus à "fermer" est toujours en cours d'exécution. 
ATTENTION : Une fois que la méthode close() a réussi, la plupart des autres méthodes et attributs de l'objet 
Process lèveront une exception ValueError.
"""
def multiprocessing_FORK_alive_close_process() : # Avec close()
    print("Exemples avec fork (par défaut linux, sous MAC, il faut le demander)")
    
    # Fera erreur : RuntimeError: context has already been set
    # multiprocessing.set_start_method('fork')
    
    print(f"Quele est le méthode de création de Processs : {multiprocessing.get_start_method()}")
    # Quele est le méthode de création de Processs : fork
    
    p = multiprocessing.Process(target=time.sleep, args=(1,))
    print("is_alive : ",p, p.is_alive())
    #<...Process ... initial> False
    p.start()
    print("is_alive : ",p, p.is_alive())
    #<...Process ... started> True
    p.join() # pour être certain que p a fini
    print("terminate : ", p.close()) # <<- close renvoie None.
    time.sleep(0.1)
    
    # ICI , ne pas utiliser is_alive, fera une exception (process is closed)
    #print("is_alive : ",p, p.is_alive())
    
    # ICI , ne pas utiliser (la lecture de) "p.exitcode", fera une exception (process object is closed)
    #print(p.exitcode == -signal.SIGTERM)
    try :
        print(p.exitcode == -signal.SIGTERM)
    except Exception as e :
        print(f"Exception levée : {e}")
"""
Exemples avec fork (par défaut linux, sous MAC, il faut le demander)
Quele est le méthode de création de Processs : fork
is_alive :  <Process name='Process-3' parent=51422 initial> False
is_alive :  <Process name='Process-3' pid=51426 parent=51422 started> True
terminate :  None
Exception levée : process object is closed        
"""
if __name__ == "__main__" :
    import platform 
    if platform.system() == 'Darwin' : # Pour Mac, demander Fork.
        multiprocessing.set_start_method('fork')
        
    print(f"0- Quele est le méthode de création de Processs : {multiprocessing.get_start_method()}")
    # Quele est le méthode de création de Processs : fork
    
    print('='*80)
    multiprocessing_FORK_alive_terminate()
    print('-'*60)
    input("On continue ? ")

    multiprocessing_SPAWN_alive_terminate()
    print('-'*60)
    input("On continue ? ")
    
    multiprocessing_FORK_alive_close_process()
