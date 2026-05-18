import os,sys 
'''N = 10 
v=1 
while os.fork()==0 and v<=N : 
    v += 1 
print(v) 
sys.exit(0)'''

for i in range(4) : 
    pid = os.fork() 
    if pid != 0 : 
        print("Ok !") 
    print("Bonjour !") 
sys.exit(0)