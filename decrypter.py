import sys
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypter():
    if len(sys.argv) < 4:
        print("Usage: python3 decrypter.py <input_filename> <key> <output_filename>")
        return

    input_filename = sys.argv[1]
    key = sys.argv[2].encode()
    output_filename = sys.argv[3]

    with open(input_filename, 'rb') as f:

        salt = f.read(16)
        iv = f.read(16)
        ciphertext = f.read()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    derived_key = kdf.derive(key)

    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    padding_length = padded_plaintext[-1]
    plaintext = padded_plaintext[:-padding_length]

    with open(output_filename, 'wb') as f:
        #f.write(plaintext)
        
        #Uncomment to see the padding
        f.write(padded_plaintext)

if __name__ == "__main__":
    decrypter()