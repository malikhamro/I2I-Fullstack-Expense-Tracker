import unittest
from encryption.rsa_encryption import generate_key_pair, load_public_key, load_private_key, encrypt_data, decrypt_data
import os

class TestRSAEncryption(unittest.TestCase):

    def setUp(self):
        # Set up file paths for testing
        self.public_key_path = 'test_public.pem'
        self.private_key_path = 'test_private.pem'
        self.sample_data = b'This is a test message.'

    def tearDown(self):
        # Clean up any generated keys
        if os.path.exists(self.public_key_path):
            os.remove(self.public_key_path)
        if os.path.exists(self.private_key_path):
            os.remove(self.private_key_path)

    def test_generate_key_pair(self):
        generate_key_pair(self.public_key_path, self.private_key_path)
        
        # Check if the key files are created
        self.assertTrue(os.path.exists(self.public_key_path))
        self.assertTrue(os.path.exists(self.private_key_path))

    def test_load_public_key(self):
        generate_key_pair(self.public_key_path, self.private_key_path)
        public_key = load_public_key(self.public_key_path)
        
        # Check if the loaded public key is valid
        self.assertIsNotNone(public_key)

    def test_load_private_key(self):
        generate_key_pair(self.public_key_path, self.private_key_path)
        private_key = load_private_key(self.private_key_path)
        
        # Check if the loaded private key is valid
        self.assertIsNotNone(private_key)

    def test_encrypt_data(self):
        generate_key_pair(self.public_key_path, self.private_key_path)
        public_key = load_public_key(self.public_key_path)
        
        encrypted_data = encrypt_data(self.sample_data, public_key)
        
        # Check if the encryption was successful by verifying the data is different
        self.assertNotEqual(self.sample_data, encrypted_data)

    def test_decrypt_data(self):
        generate_key_pair(self.public_key_path, self.private_key_path)
        public_key = load_public_key(self.public_key_path)
        private_key = load_private_key(self.private_key_path)
        
        encrypted_data = encrypt_data(self.sample_data, public_key)
        decrypted_data = decrypt_data(encrypted_data, private_key)
        
        # Check if the decrypted data matches the original data
        self.assertEqual(self.sample_data, decrypted_data)

if __name__ == '__main__':
    unittest.main()
