# Somme avec Pool
import multiprocessing as mp 
import time,os

# Define a function for the Process
def somme(args) :
    ProcessName, deb, fin = args
    #print(f"Je suis {ProcessName} et je fais la somme de {deb} à {fin}")
    print(f"Je suis {mp.current_process().name} et je fais la somme de {deb} à {fin}")
    S_local=0
    for i in range(deb, fin) :
        S_local += L[i]
    return  S_local

if __name__ == "__main__" :
    import platform
    if platform.system() == 'Darwin' :
        mp.set_start_method('fork')
        
    N=1000000
    nb_tranches = (N//9) %8 +1
    L=[1 for _ in range(N)]  # Initialisation  
#    nb_tranches = os.cpu_count() -2
    params = [(f"P{str(i)}" , i*N//nb_tranches, (i+1)*N//nb_tranches) for i in range(nb_tranches)]
    t_start = time.time_ns()
    # De manière équivalente :
    # with mp.Pool(nb_tranches) as p : resultats=p.map(somme, params)    

    resultats = mp.Pool(3).map(somme, params) 
    somme_finale = sum(resultats)
    t_end = time.time_ns()
    print(f"{somme_finale=} en {str((t_end - t_start)/1000000000)} ns")

"""    
Je suis ForkPoolWorker-1 et je fais la somme de 0 à 125000
Je suis ForkPoolWorker-2 et je fais la somme de 125000 à 250000
Je suis ForkPoolWorker-3 et je fais la somme de 250000 à 375000
Je suis ForkPoolWorker-1 et je fais la somme de 375000 à 500000
Je suis ForkPoolWorker-3 et je fais la somme de 500000 à 625000
Je suis ForkPoolWorker-2 et je fais la somme de 625000 à 750000
Je suis ForkPoolWorker-1 et je fais la somme de 750000 à 875000
Je suis ForkPoolWorker-2 et je fais la somme de 875000 à 1000000
somme_finale=1000000 en 0.043934927 ns
"""
    
