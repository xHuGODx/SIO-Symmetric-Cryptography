import sys
import os
from PIL import Image
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypter():
    if len(sys.argv) < 4:
        print("Usage: python3 encrypterCBC.py <input_image> <key> <output_image>")
        return

    input_image = sys.argv[1]
    key = sys.argv[2].encode()
    output_image = sys.argv[3]

    salt = os.urandom(16)
    iv = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    derived_key = kdf.derive(key)

    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    img = Image.open(input_image)
    img = img.convert("RGB")
    pixels = list(img.getdata())

    pixel_bytes = bytes([component for pixel in pixels for component in pixel])

    padding_length = 16 - (len(pixel_bytes) % 16)
    padded_pixel_bytes = pixel_bytes + bytes([padding_length] * padding_length)

    encrypted_pixels = encryptor.update(padded_pixel_bytes) + encryptor.finalize()

    encrypted_pixels = [
        tuple(encrypted_pixels[i:i+3]) for i in range(0, len(encrypted_pixels) - padding_length, 3)
    ]

    encrypted_img = Image.new(img.mode, img.size)
    encrypted_img.putdata(encrypted_pixels)

    encrypted_img.save(output_image)

    with open(input_image, 'rb') as original_file:
        original_header = original_file.read(54)

    with open(output_image, 'r+b') as encrypted_file:
        encrypted_file.seek(0)
        encrypted_file.write(original_header)

    with open(output_image + '.meta', 'wb') as meta_file:
        meta_file.write(salt + iv)

if __name__ == "__main__":
    encrypter()