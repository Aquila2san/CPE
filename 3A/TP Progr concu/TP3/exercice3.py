import os
import sys

def main():
    # Tubes pour envoyer les nombres depuis le générateur
    r_pair, w_pair = os.pipe()
    r_impair, w_impair = os.pipe()
    
    # Tubes pour renvoyer les sommes au générateur
    r_spair, w_spair = os.pipe()
    r_simpair, w_simpair = os.pipe()

    # Fork 1 : Filtre Pair
    pid1 = os.fork()
    if pid1 == 0:
        os.close(w_pair); os.close(r_spair); os.close(r_impair); os.close(w_impair); os.close(r_simpair); os.close(w_simpair)
        f_in = os.fdopen(r_pair, 'r')
        f_out = os.fdopen(w_spair, 'w')
        somme = 0
        for ligne in f_in:
            val = int(ligne.strip())
            if val == -1: break
            somme += val
        f_out.write(f"{somme}\n")
        f_out.close(); f_in.close()
        sys.exit(0)

    # Fork 2 : Filtre Impair
    pid2 = os.fork()
    if pid2 == 0:
        os.close(r_pair); os.close(w_pair); os.close(r_spair); os.close(w_spair); os.close(w_impair); os.close(r_simpair)
        f_in = os.fdopen(r_impair, 'r')
        f_out = os.fdopen(w_simpair, 'w')
        somme = 0
        for ligne in f_in:
            val = int(ligne.strip())
            if val == -1: break
            somme += val
        f_out.write(f"{somme}\n")
        f_out.close(); f_in.close()
        sys.exit(0)

    # Processus Parent : Générateur de nombres
    os.close(r_pair); os.close(r_impair); os.close(w_spair); os.close(w_simpair)
    f_pair = os.fdopen(w_pair, 'w')
    f_impair = os.fdopen(w_impair, 'w')
    
    import random
    N = 10  # Exemple de quantité
    print(f"[Générateur] Génération de {N} nombres...")
    for _ in range(N):
        num = random.randint(0, 100)
        if num % 2 == 0:
            f_pair.write(f"{num}\n")
        else:
            f_impair.write(f"{num}\n")
            
    # Signal de fin
    f_pair.write("-1\n"); f_impair.write("-1\n")
    f_pair.close(); f_impair.close()

    # Récupération des résultats
    f_spair = os.fdopen(r_spair, 'r')
    f_simpair = os.fdopen(r_simpair, 'r')
    
    s_pair = int(f_spair.read().strip())
    s_impair = int(f_simpair.read().strip())
    
    f_spair.close(); f_simpair.close()
    
    print(f"Somme des pairs : {s_pair}")
    print(f"Somme des impairs : {s_impair}")
    print(f"Somme totale : {s_pair + s_impair}")
    
    os.wait(); os.wait()

if __name__ == "__main__":
    main()