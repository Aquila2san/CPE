import os
import sys

commandes = [["who"], ["ps"], ["ls", "-l"]]

for cmd in commandes:
    if os.fork() == 0:
        os.execlp(cmd[0], *cmd)
        sys.exit(1)

for _ in commandes:
    os.wait()
    