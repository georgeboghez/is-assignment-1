from multiprocessing.connection import Client
from config import PORT1, PASSWD, KEY3

address = ('localhost', PORT1)
conn = Client(address, authkey=PASSWD)

key1 = ''

while not conn.closed:
    msg = input()
    conn.send(msg)
    if msg == 'close' or msg == 'close listener':
        conn.close()
    elif msg == 'cfb' or msg == 'ebc':
        key1 = conn.recv()
        print(key1)
        conn.close()