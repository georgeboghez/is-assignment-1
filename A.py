from multiprocessing.connection import Client
from config import PORT1, PORT2, PASSWD, KEY3, IV, BLOCKSIZE
from Crypto.Cipher import AES


def ecnrypt_data(decrypted_key, chunk_to_encrypt):
    cipher = AES.new(decrypted_key, AES.MODE_ECB, IV)
    return cipher.encrypt(chunk_to_encrypt * 16)


def use_ecb(conn, decrypted_key):
    with open('keys.bin', 'rb') as f:
        while True:
            chunk = f.read(BLOCKSIZE)
            if not chunk:
                break
            encr_data = ecnrypt_data(decrypted_key, chunk)
            conn.send(encr_data)


def use_cfb(conn, decrypted_key):
    cipher = AES.new(decrypted_key, AES.MODE_CFB, IV)
    initialIV = IV
    with open("landscape.bmp", "rb") as f:
        while True:
            plaintext = f.read(BLOCKSIZE)
            if not plaintext:
                break
            encrypted_iv = cipher.encrypt(initialIV)
            ciphertext = bytes(
                [b1 ^ b2 for b1, b2 in zip(plaintext, encrypted_iv)])
            # plain_decr = bytes([b1 ^ b2 for b1, b2 in zip(encrypted_iv, ciphertext)])
            conn.send(ciphertext)
            initialIV = ciphertext


def communicate(conn, decrypted_key, mode):
    if mode == 'ecb':
        use_ecb(conn, decrypted_key)
    elif mode == 'cfb':
        use_cfb(conn, decrypted_key)


if __name__ == "__main__":
    address = ('127.0.0.1', PORT1)
    conn = Client(address, authkey=PASSWD)

    print("Connected to KM")

    while not conn.closed:
        msg = input()
        conn.send(msg)
        if msg == 'close' or msg == 'close listener':
            conn.close()
        elif msg == 'cfb' or msg == 'ecb':
            if msg == 'cfb':
                mode = 'cfb'
            else:
                mode = 'ecb'
            key = conn.recv()
            conn.close()

    print('key:', key)
    print('mode:', mode)

    if mode == 'cfb':
        cipher = AES.new(KEY3, AES.MODE_CFB, IV)
    elif mode == 'ecb':
        cipher = AES.new(KEY3, AES.MODE_ECB, IV)

    decrypted_key = cipher.decrypt(key)

    print('decrypted_key:', decrypted_key)

    address = ('127.0.0.1', PORT2)
    conn = Client(address, authkey=PASSWD)

    print("Connected to B")

    conn.send(key)
    conn.send(mode)

    msg = conn.recv()
    if msg == 'beginning message':
        communicate(conn, decrypted_key, mode)
        msg = b'done'
        conn.send(msg)
        if msg == b'done' or msg == 'close listener':
            conn.close()
    else:
        print("couldn't begin the communication. didn't receive the corresponding message")
        conn.close()
