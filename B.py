from multiprocessing.connection import Client
from config import PORT2, PASSWD, KEY3

def readFile(filename="Laborator2A.txt"):
    with open(filename, mode="r", encoding="utf8") as f:
        content = f.readline()
        while len(content) != 0:
            print(content)
            content = f.readline()

readFile()
print(len(KEY3))