import sys
import base64
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypter():
    if len(sys.argv) < 4:
        print("Usage: python3 encrypter.py <input_filename> <key> <output_filename>")
        return

    input_filename = sys.argv[1]
    key = sys.argv[2].encode() 
    output_filename = sys.argv[3]

    #Uncomment to use random key

    #key = os.urandom(32)
    #key = os.urandom(16)
    
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    derived_key = kdf.derive(key)

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_filename, 'rb') as f:
        plaintext = f.read()


    padding_length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext + bytes([padding_length] * padding_length)

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    with open(output_filename, 'wb') as f:
        f.write(salt + iv + ciphertext)

if __name__ == "__main__":
    encrypter()