import sys
import os
from PIL import Image
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypter():
    if len(sys.argv) < 4:
        print("Usage: python3 decrypterECB.py <input_image> <key> <output_image>")
        return

    input_image = sys.argv[1]
    key = sys.argv[2].encode()
    output_image = sys.argv[3]

    with open(input_image, 'rb') as f:
        salt = f.read(16)
        encrypted_pixel_bytes = f.read()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    derived_key = kdf.derive(key)

    cipher = Cipher(algorithms.AES(derived_key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_pixel_bytes = decryptor.update(encrypted_pixel_bytes) + decryptor.finalize()

    padding_length = padded_pixel_bytes[-1]
    pixel_bytes = padded_pixel_bytes[:-padding_length]

    decrypted_pixels = [
        tuple(pixel_bytes[i:i+3]) for i in range(0, len(pixel_bytes), 3)
    ]

    img = Image.open(input_image)
    img = img.convert("RGB")

    decrypted_img = Image.new(img.mode, img.size)
    decrypted_img.putdata(decrypted_pixels)
    decrypted_img.save(output_image)

if __name__ == "__main__":
    decrypter()