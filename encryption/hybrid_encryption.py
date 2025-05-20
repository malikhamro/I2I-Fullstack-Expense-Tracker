import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

AES_KEY_SIZE = 32  # AES key size in bytes
RSA_KEY_SIZE = 2048  # RSA key size in bits
BLOCK_SIZE = 16  # Block size for AES

# Generates a new hybrid encryption key pair using AES and RSA
def generate_hybrid_key_pair():
    try:
        # Generate AES key
        aes_key = get_random_bytes(AES_KEY_SIZE)

        # Generate RSA key pair
        rsa_key = RSA.generate(RSA_KEY_SIZE)
        private_key = rsa_key.export_key()
        public_key = rsa_key.publickey().export_key()

        # Save keys to files
        with open("aes_key.bin", "wb") as aes_file:
            aes_file.write(aes_key)
        with open("private_key.pem", "wb") as private_file:
            private_file.write(private_key)
        with open("public_key.pem", "wb") as public_file:
            public_file.write(public_key)

        return aes_key, private_key, public_key
    except Exception as e:
        raise RuntimeError(f"Failed to generate hybrid key pair: {str(e)}")

# Encrypts data using hybrid encryption (combination of AES and RSA)
def encrypt_data_hybrid(data, public_key_file):
    try:
        # Load public key
        with open(public_key_file, "rb") as public_file:
            public_key = RSA.import_key(public_file.read())
        
        # Generate AES session key
        aes_session_key = get_random_bytes(AES_KEY_SIZE)
        
        # Encrypt the data using AES
        cipher_aes = AES.new(aes_session_key, AES.MODE_CBC)
        encrypted_data = cipher_aes.encrypt(pad(data, BLOCK_SIZE))
        
        # Encrypt the AES session key using RSA
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted_session_key = cipher_rsa.encrypt(aes_session_key)
        
        return encrypted_session_key, cipher_aes.iv, encrypted_data
    except Exception as e:
        raise RuntimeError(f"Failed to encrypt data using hybrid encryption: {str(e)}")

# Decrypts data using hybrid encryption (combination of AES and RSA)
def decrypt_data_hybrid(encrypted_session_key, iv, encrypted_data, private_key_file):
    try:
        # Load private key
        with open(private_key_file, "rb") as private_file:
            private_key = RSA.import_key(private_file.read())
        
        # Decrypt the AES session key using RSA
        cipher_rsa = PKCS1_OAEP.new(private_key)
        aes_session_key = cipher_rsa.decrypt(encrypted_session_key)
        
        # Decrypt the data using AES
        cipher_aes = AES.new(aes_session_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher_aes.decrypt(encrypted_data), BLOCK_SIZE)
        
        return decrypted_data
    except Exception as e:
        raise RuntimeError(f"Failed to decrypt data using hybrid encryption: {str(e)}")

if __name__ == "__main__":
    # Example usage
    aes_key, private_key, public_key = generate_hybrid_key_pair()

    message = b"Secret Message"

    encrypted_session_key, iv, encrypted_data = encrypt_data_hybrid(message, "public_key.pem")

    decrypted_data = decrypt_data_hybrid(encrypted_session_key, iv, encrypted_data, "private_key.pem")

    print("Original message:", message)
    print("Decrypted message:", decrypted_data)
