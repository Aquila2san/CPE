import sys

arg = sys.argv[1:]

if len(arg) == 0:
    print("Aucune moyenne à calculer")

else:
    a = len(arg)
    b = 0
    for i in range(len(arg)):
        try:
            if int(arg[i]) < 0 or int(arg[i]) > 20:
                print("Note(s) non valide(s)")
                sys.exit(0) 
                
            b += int(arg[i])
            
        except ValueError:
            print("Note(s) non valide(s)")
            sys.exit(0)
    print("Moyenne :", "%.2f" %(b/a))
    
