from multiprocessing.connection import Listener
from config import PORT1, PASSWD, KEY3, IV
from Crypto.Cipher import AES
from os import urandom


def generateKey():
    key = urandom(16)
    cipher = AES.new(KEY3, AES.MODE_CFB, IV)
    try:
        with open("keys.bin", "w+") as f:
            f.write(str(key))
    except Exception as e:
        print('Failed to write: ' + str(e))

    return cipher.encrypt(key)


if __name__ == '__main__':
    address = ('127.0.0.1', PORT1)
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
            elif msg == 'cfb' or msg == 'ecb':
                conn.send(generateKey())
                conn.close()
        print("Connection closed")
    print("Listener closed")
