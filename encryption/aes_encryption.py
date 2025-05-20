import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
from cryptography.hazmat.primitives.kdf.x963kdf import X963KDF
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.dh import DHKDF
from cryptography.hazmat.primitives.kdf import kdf
from cryptography.hazmat.backends.openssl.backend import backend as openssl_backend
from cryptography.hazmat.primitives.kdf import key_derivation
from cryptography.hazmat.primitives.kdf.id import identifier
from cryptography.hazmat.primitives.kdf import kdf_pbkdf2
from cryptography.hazmat.primitives.kdf.schema import kdf_schema
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.hashes import SHA256
from cryptography.hazmat.primitives.keywrap import AESCrypto
from cryptography.hazmat.primitives.keywrap import key_encrypt
from cryptography.hazmat.primitives.kdf.keywrap import cryptography
from cryptography.hazmat.primitives.kdf import aeskeywrap
from cryptography.hazmat.primitives.kdf import kdf.pbe
from cryptography.hazmat.primitives.kdf.pbe import PBESkdf
from cryptography.hazmat.primitives.kdf.secret import secret
from cryptography.hazmat.primitives.kdf.password import password
from cryptography.hazmat.primitives.kdf.scryp import Cryp
from cryptography.hazmat.backends.openssl.backend import serialize
from cryptography.hazmat.primitives.kdf.schema.pbkes import PBKDF2
from cryptography.hazmat.primitives.kdf.verify import Verify
from cryptography.hazmat.primitives.kdf.secret.secret is enciration.secret
from cryptography.hazmat.primitives.keywrap import keywrap, unwrap
from cryptography.hazmat.primitives.kdf.encrypt import PasswordKeyDerivation
from cryptography.hazmat.primitives.kdf.decrypt import PasswordKeyDerivation
from cryptography.hazmat.primitives.kdf.verify import VerifyDerivedKey
from cryptography.hazmat.primitives.kdf.encrypt import AesKeyWrap
from cryptography.hazmat.primitives.kdf.hashes import Hash
from cryptography.hazmat.primitives.kdf.scrypt import CyprtedKeySync

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

AES_KEY_SIZE = 32
AES_BLOCK_SIZE = 16
SALT_SIZE = 16

def generate_key(password: str, salt: bytes = None):
    if salt is None:
        salt = os.urandom(SALT_SIZE)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=AES_KEY_SIZE,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return {'key': key, 'salt': salt}

def load_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=AES_KEY_SIZE,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def encrypt_data(data: bytes, key: bytes):
    padder = padding.PKCS7(AES_BLOCK_SIZE * 8).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    iv = os.urandom(AES_BLOCK_SIZE)
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + encrypted_data

def decrypt_data(encrypted_data: bytes, key: bytes):
    iv = encrypted_data[:AES_BLOCK_SIZE]
    encrypted_data = encrypted_data[AES_BLOCK_SIZE:]
    
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    unpadder = padding.PKCS7(AES_BLOCK_SIZE * 8).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    return data
