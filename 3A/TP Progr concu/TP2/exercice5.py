import os
import sys
import time

N = int(sys.argv[1]) 

for i in range(N):
    pid = os.fork() 
    
    if pid == 0:
        print(f"Fils {i}: Mon PID = {os.getpid()}, PID de mon père = {os.getppid()}") 
        time.sleep(2 * i) 
        print(f"Fils {i}: Fin de l'attente")
        sys.exit(i) 

for _ in range(N):
    pid_fils, etat = os.wait() 
    code_retour = os.waitstatus_to_exitcode(etat) if hasattr(os, 'waitstatus_to_exitcode') else (etat >> 8)
    print(f"Père: Le processus fils {pid_fils} s'est terminé avec l'état {code_retour}") 