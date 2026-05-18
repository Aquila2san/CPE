import os
import sys

for i in range(3): 
    retour = os.fork()
    pid = os.getpid()
    ppid = os.getppid()
    print(f"(i : {i}) je suis le processus : {os.getpid()}, mon pere est : {os.getppid()}, retour : {retour} ")