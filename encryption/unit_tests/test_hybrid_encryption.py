import unittest
from encryption.hybrid_encryption import generate_hybrid_key_pair, encrypt_data_hybrid, decrypt_data_hybrid

class TestHybridEncryption(unittest.TestCase):

    def setUp(self):
        self.aes_key, self.rsa_key_pair = generate_hybrid_key_pair()
        self.data = b"Test data for hybrid encryption"
    
    def test_generate_hybrid_key_pair(self):
        # Generate hybrid key pair
        aes_key, rsa_key_pair = generate_hybrid_key_pair()
        
        # Check if AES key is 256 bits (32 bytes)
        self.assertEqual(len(aes_key), 32, "AES key length is incorrect.")
        
        # Check if RSA private key and public key exist
        self.assertIsNotNone(rsa_key_pair.privatekey(), "RSA private key is not generated.")
        self.assertIsNotNone(rsa_key_pair.publickey(), "RSA public key is not generated.")

    def test_encrypt_data_hybrid(self):
        ciphertext = encrypt_data_hybrid(self.data, self.aes_key, self.rsa_key_pair.publickey())
        
        # Ensure that ciphertext is not None
        self.assertIsNotNone(ciphertext, "Hybrid encryption failed, ciphertext is None.")
        
        # Ensure that ciphertext is bytes
        self.assertIsInstance(ciphertext, bytes, "Ciphertext is not in bytes format.")

    def test_decrypt_data_hybrid(self):
        ciphertext = encrypt_data_hybrid(self.data, self.aes_key, self.rsa_key_pair.publickey())
        decrypted_data = decrypt_data_hybrid(ciphertext, self.aes_key, self.rsa_key_pair.privatekey())
        
        # Ensure the decrypted data matches the original data
        self.assertEqual(decrypted_data, self.data, "Decryption failed, data does not match original.")
        
        # Ensure that decrypted data is bytes
        self.assertIsInstance(decrypted_data, bytes, "Decrypted data is not in bytes format.")

if __name__ == '__main__':
    unittest.main()
