from aes import encrypt_message, decrypt_message

if __name__ == "__main__":
    message = "This is a secret message!"
    password = "strongpassword123"

    print("Original message:", message)
    encrypted = encrypt_message(message, password)
    print("Encrypted (base64):", encrypted.hex())

    decrypted = decrypt_message(encrypted, password)
    print("Decrypted message:", decrypted)

    assert decrypted == message, "Decryption failed!"
    print("Test passed!") 