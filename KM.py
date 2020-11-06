from multiprocessing.connection import Listener
from config import PORT, PASSWD

address = ('localhost', PORT)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=PASSWD)
conn = listener.accept()
print('Connection accepted from', listener.last_accepted)
while True:
    msg = conn.recv()
    # do something with msg
    print(msg)
    if msg == 'close':
        conn.close()
        break
listener.close()