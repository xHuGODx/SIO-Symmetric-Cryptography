import sys
import os
from PIL import Image
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypter():
    if len(sys.argv) < 4:
        print("Usage: python3 decrypterCBC.py <encrypted_image> <key> <output_image>")
        return

    encrypted_image = sys.argv[1]
    key = sys.argv[2].encode()
    output_image = sys.argv[3]

    # Read metadata (salt and IV) from the .meta file
    with open(encrypted_image + '.meta', 'rb') as meta_file:
        salt = meta_file.read(16)
        iv = meta_file.read(16)

    # Derive the key using PBKDF2
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

    # Open the encrypted image
    img = Image.open(encrypted_image)
    pixels = list(img.getdata())

    # Convert the pixel data back to bytes
    pixel_bytes = bytes([component for pixel in pixels for component in pixel])

    # Decrypt the pixel data
    decrypted_pixel_bytes = decryptor.update(pixel_bytes) + decryptor.finalize()

    # Remove padding
    padding_length = decrypted_pixel_bytes[-1]
    decrypted_pixel_bytes = decrypted_pixel_bytes[:-padding_length]

    # Rebuild the pixel data from the decrypted bytes
    decrypted_pixels = [
        tuple(decrypted_pixel_bytes[i:i+3]) for i in range(0, len(decrypted_pixel_bytes), 3)
    ]

    # Create a new image with the decrypted data
    decrypted_img = Image.new(img.mode, img.size)
    decrypted_img.putdata(decrypted_pixels)

    # Restore the original header from the encrypted image
    with open(encrypted_image, 'rb') as encrypted_file:
        original_header = encrypted_file.read(54)

    with open(output_image, 'wb') as output_file:
        output_file.write(original_header)

    decrypted_img.save(output_image)

if __name__ == "__main__":
    decrypter()
