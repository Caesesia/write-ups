#!/usr/bin/python3 -u

import sys, base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

import mysecrets

def encrypt_message_ecb(plaintext):
    cipher = Cipher(algorithms.AES(mysecrets.key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext + mysecrets.flag) + padder.finalize()
    return encryptor.update(padded_data) + encryptor.finalize()

if __name__ == "__main__":
    try:
        for line in sys.stdin:
            line=line.rstrip()
            sys.stdout.write(base64.b64encode(encrypt_message_ecb(line.encode())).decode()+"\n")
    except:
        pass

