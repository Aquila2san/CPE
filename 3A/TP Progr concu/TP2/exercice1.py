import os
import sys

pid = os.fork()

if not pid:
    pid = os.fork()

print(pid)

    