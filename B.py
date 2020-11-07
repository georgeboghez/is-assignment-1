from multiprocessing.connection import Listener
from config import PORT2, PASSWD, IV, KEY3, BLOCKSIZE
from Crypto.Cipher import AES


def decrypt_using_ecb(decrypted_key, chunk_to_decrypt):
    cipher = AES.new(decrypted_key, AES.MODE_ECB, IV)
    return cipher.decrypt(chunk_to_decrypt)[0:int(len(chunk_to_decrypt) / 16)]


def receive_key_and_mode(conn):
    key = conn.recv()
    mode = conn.recv()
    return (key, mode)


def get_decrypted_key(key, mode):
    if mode == 'cfb':
        cipher = AES.new(KEY3, AES.MODE_CFB, IV)
    elif mode == 'ecb':
        cipher = AES.new(KEY3, AES.MODE_ECB, IV)
    return cipher.decrypt(key)


def use_ecb(conn, decrypted_key):
    with open("k.bin", "wb+") as f:
        msg = conn.recv()
        while msg != b'done':
            decr_msg = decrypt_using_ecb(decrypted_key, msg)
            bytesWritten = f.write(decr_msg)
            print('bytesWritten:', bytesWritten)
            msg = conn.recv()


def use_cfb(conn, decrypted_key):
    cipher = AES.new(decrypted_key, AES.MODE_CFB, IV)
    initialIV = IV
    with open("k.bmp", "wb+") as f:
        msg = conn.recv()
        while msg != b'done':
            encrypted_iv = cipher.encrypt(initialIV)
            plaintext = bytes([b1 ^ b2 for b1, b2 in zip(msg, encrypted_iv)])
            bytesWritten = f.write(plaintext)
            print('bytesWritten:', bytesWritten)
            initialIV = msg
            msg = conn.recv()


def communicate(conn, decrypted_key, mode):
    if mode == 'cfb':
        use_cfb(conn, decrypted_key)
    elif mode == 'ecb':
        use_ecb(conn, decrypted_key)


if __name__ == '__main__':
    address = ('127.0.0.1', PORT2)
    listener = Listener(address, authkey=PASSWD)
    conn = listener.accept()

    print('Connection accepted from', listener.last_accepted)

    key, mode = receive_key_and_mode(conn)
    decrypted_key = get_decrypted_key(key, mode)

    print('key:', key)
    print('mode:', mode)
    print("decrypted_key:", decrypted_key)

    conn.send('beginning message')
    communicate(conn, decrypted_key, mode)
    conn.close()
    print("Connection closed")
    listener.close()
    print("Listener closed")
