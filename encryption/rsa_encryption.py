import rsa
import os

def generate_key_pair(key_size=2048):
    """Generates a new RSA encryption key pair."""
    try:
        public_key, private_key = rsa.newkeys(key_size)
        with open("public_key.pem", "wb") as pub_file:
            pub_file.write(public_key.save_pkcs1('PEM'))
        with open("private_key.pem", "wb") as priv_file:
            priv_file.write(private_key.save_pkcs1('PEM'))
        return "Keys generated and saved successfully."
    except Exception as e:
        return f"An error occurred while generating the key pair: {e}"

def load_public_key(file_path):
    """Loads an existing RSA public key from a file."""
    try:
        with open(file_path, "rb") as pub_file:
            public_key_data = pub_file.read()
        public_key = rsa.PublicKey.load_pkcs1(public_key_data)
        return public_key
    except FileNotFoundError:
        return "Public key file not found."
    except Exception as e:
        return f"An error occurred while loading the public key: {e}"

def load_private_key(file_path):
    """Loads an existing RSA private key from a file."""
    try:
        with open(file_path, "rb") as priv_file:
            private_key_data = priv_file.read()
        private_key = rsa.PrivateKey.load_pkcs1(private_key_data)
        return private_key
    except FileNotFoundError:
        return "Private key file not found."
    except Exception as e:
        return f"An error occurred while loading the private key: {e}"

def encrypt_data(data, public_key):
    """Encrypts data using the provided RSA public key."""
    try:
        encrypted_data = rsa.encrypt(data.encode('utf-8'), public_key)
        return encrypted_data
    except Exception as e:
        return f"An error occurred while encrypting the data: {e}"

def decrypt_data(encrypted_data, private_key):
    """Decrypts data using the provided RSA private key."""
    try:
        decrypted_data = rsa.decrypt(encrypted_data, private_key).decode('utf-8')
        return decrypted_data
    except Exception as e:
        return f"An error occurred while decrypting the data: {e}"
