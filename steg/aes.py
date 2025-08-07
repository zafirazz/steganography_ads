from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64

# Constants
SALT_SIZE = 16  # 128-bit salt
KEY_SIZE = 32   # 256-bit key
IV_SIZE = 16    # 128-bit IV
PBKDF2_ITERATIONS = 100_000


def pad(data: bytes) -> bytes:
    padding_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([padding_len] * padding_len)

def unpad(data: bytes) -> bytes:
    padding_len = data[-1]
    if padding_len < 1 or padding_len > AES.block_size:
        raise ValueError("Invalid padding")
    return data[:-padding_len]

def encrypt_message(message: str, password: str) -> bytes:
    salt = get_random_bytes(SALT_SIZE)
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=PBKDF2_ITERATIONS)
    iv = get_random_bytes(IV_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(message.encode('utf-8'))
    ciphertext = cipher.encrypt(padded)
    # Store as: salt + iv + ciphertext
    return salt + iv + ciphertext

def decrypt_message(ciphertext: bytes, password: str) -> str:
    salt = ciphertext[:SALT_SIZE]
    iv = ciphertext[SALT_SIZE:SALT_SIZE+IV_SIZE]
    ct = ciphertext[SALT_SIZE+IV_SIZE:]
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=PBKDF2_ITERATIONS)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = cipher.decrypt(ct)
    message = unpad(padded)
    return message.decode('utf-8') 