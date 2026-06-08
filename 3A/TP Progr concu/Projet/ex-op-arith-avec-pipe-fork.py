# Nov 2020 : exemple fork  
# CPE concurrent Python  
# Le pere demande au fils de faires des opération arith et de lui rendre les résultats

#import multiprocessing as mp

#def je_fais_des_calculs_avec_bc(commande : str) :
    
    #os.execlp("echo ")
    

#def je_fais_des_calculs_moi_meme(commande : str) :
    
import time,os,random
 
def fils_calculette(rpipe_commande, wpipe_reponse):
    print('Bonjour du Fils', os.getpid())
      
    while True:
        cmd = os.read(rpipe_commande, 32)
        print("Le fils a recu ", cmd.decode())
        res=eval(cmd)
        print("Dans fils, le résultat =", res)
        os.write(wpipe_reponse, str(res).encode())
        print("Le fils a envoyé", res)
        time.sleep(1)

    os._exit(0)
        
def parent():
    rpipe_reponse, wpipe_reponse = os.pipe()
    rpipe_commande, wpipe_commande = os.pipe()
    pid = os.fork()
    if pid == 0:
        fils_calculette(rpipe_commande, wpipe_reponse)
        assert False, 'fork du fils n a pas marché !'
    else :
        os.close(wpipe_reponse)
        os.close(rpipe_commande)        
        while True :
            # Le pere envoie au fils un calcul à faire et récupère le résultat
            opd1 = random.randint(1,10)
            opd2 = random.randint(1,10)
            operateur=random.choice(['+', '-', '*', '/'])
            str_commande = str(opd1) + operateur + str(opd2)
            
            os.write(wpipe_commande, str_commande.encode())
            print("Le père va demander à faire : ", str_commande)
            res = os.read(rpipe_reponse, 32)
            print("Le Pere a recu ", res.decode())
            print('-'* 60)
            time.sleep(1)
            
    #else:
        #os.close(wpipe_reponse)
        #print('hello from parent', os.getpid(), pid)
        #fobj = os.fdopen(rpipe_reponse, 'r')
        #while True:
            #recv = os.read(rpipe_reponse, 32)
            #print recv
if __name__ == "__main__" :
    import platform, multiprocessing as mp
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
    parent()

"""
TRACE :
Le père va demander à faire :  5/9
Bonjour du Fils 12851
Le fils a recu  5/9
Dans fils, le résultat = 0.5555555555555556
Le fils a envoyé 0.5555555555555556
Le Pere a recu  0.5555555555555556
------------------------------------------------------------
Le père va demander à faire :  5/2
Le fils a recu  5/2
Dans fils, le résultat = 2.5
Le fils a envoyé 2.5
Le Pere a recu  2.5
------------------------------------------------------------
Le père va demander à faire :  8*6
Le fils a recu  8*6
Dans fils, le résultat = 48
Le fils a envoyé 48
Le Pere a recu  48
------------------------------------------------------------
Le père va demander à faire :  8-8
Le fils a recu  8-8
Dans fils, le résultat = 0
Le fils a envoyé 0
Le Pere a recu  0
------------------------------------------------------------
Le père va demander à faire :  9-8
Le fils a recu  9-8
Dans fils, le résultat = 1
Le fils a envoyé 1
Le Pere a recu  1
------------------------------------------------------------


"""