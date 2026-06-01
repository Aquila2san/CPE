import multiprocessing as mp 
import os , sys 
msg= "monMessage" 
print("Création d’un pipe anonyme") 
(dfr, dfw) = mp.Pipe() 
n = dfw.send(msg) #je dépose msgdans le tube 
print("Le processus %d a transmis le message %s\n"  %(os.getpid() , msg) ) 
msgReception= dfr.recv() 
print("Le processus %d a reçu le message %s\n" %(os.getpid() , msgReception)) 
dfr.close( ) ; dfw.close( ) 
sys.exit(0)