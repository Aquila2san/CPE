import os
import sys

pid1 = os.fork()

if pid1 == 0:
    for i in range(1, 101):
        print(i)
    sys.exit(0)

pid2 = os.fork()

if pid2 == 0:
    for i in range(101, 201):
        print(i)
    sys.exit(0)

os.waitpid(pid1, 0)
os.waitpid(pid2, 0)