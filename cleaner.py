from config import PORT1, PASSWD
from multiprocessing.connection import Client


if __name__ == "__main__":
    address = ('127.0.0.1', PORT1)
    conn = Client(address, authkey=PASSWD)

    print("Connected to KM")

    while not conn.closed:
        msg = 'close listener'
        conn.send(msg)
        conn.close()
    print("Connection closed")