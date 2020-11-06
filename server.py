from multiprocessing.connection import Listener
from config import PORT1, PASSWD
from Crypto.Cipher import AES
from os import urandom

def generateKey(mode='cfb'):
    return urandom(16)

address = ('localhost', PORT1)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=PASSWD)
isListenerClosed = True
while isListenerClosed:
    conn = listener.accept()
    print('Connection accepted from', listener.last_accepted)
    while not conn.closed:
        msg = conn.recv()
        print(msg)
        if msg == 'close':
            conn.close()
        elif msg == 'close listener':
            conn.close()
            isListenerClosed = False
        elif msg == 'cfb' or msg == 'ebc':
            conn.send(generateKey())
            conn.close()