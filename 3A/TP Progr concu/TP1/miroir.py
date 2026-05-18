import sys

chaine = sys.argv[1]
a = ''
for i in range(1, len(chaine) + 1):
    a += chaine[-i]
print(a)