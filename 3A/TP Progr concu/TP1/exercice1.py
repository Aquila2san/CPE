import sys 
print("Nom du programme : ", sys.argv[0]) 
print("Nombre d'arguments : ", len(sys.argv)-1) 
print("Les arguments sont : ") 
for argument in sys.argv[1:] : 
    print(argument)
print(sys.argv)