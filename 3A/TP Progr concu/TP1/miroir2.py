import sys

l = []

for k in range(len(sys.argv) - 1):    
    chaine = sys.argv[k+1]
    a = ''
    for i in range(1, len(chaine) + 1):
        a += chaine[-i]
    l.append(a)
    
print(l)