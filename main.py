import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend

# Key derivation function
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt function
def encrypt(plain_text: str, password: str) -> (str, str):
    # Generate a random salt
    salt = os.urandom(16)
    key = derive_key(password, salt)

    # Generate a random IV
    iv = os.urandom(16)

    # Pad the plaintext
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()

    # Encrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    # Encode to Base64 for safe transport
    return base64.b64encode(salt + iv + cipher_text).decode(), base64.b64encode(salt).decode()

# Decrypt function
def decrypt(cipher_text: str, password: str) -> str:
    decoded_data = base64.b64decode(cipher_text)

    # Extract the salt, IV, and cipher text
    salt = decoded_data[:16]
    iv = decoded_data[16:32]
    cipher_text = decoded_data[32:]

    key = derive_key(password, salt)

    # Decrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plain_text = decryptor.update(cipher_text) + decryptor.finalize()

    # Unpad the plaintext
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain_text = unpadder.update(padded_plain_text) + unpadder.finalize()

    return plain_text.decode()

# Example usage
password = "securepassword"
message = "This is a secret message!"

# Encrypt
cipher_text, salt = encrypt(message, password)
print("Encrypted:", cipher_text)
print("Salt (Base64):", salt)

# Decrypt
decrypted_message = decrypt(cipher_text, password)
print("Decrypted:", decrypted_message)