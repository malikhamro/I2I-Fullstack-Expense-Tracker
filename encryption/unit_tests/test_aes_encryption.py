import unittest
from encryption.aes_encryption import generate_key, load_key, encrypt_data, decrypt_data
import os


class TestAESEncryption(unittest.TestCase):

    def setUp(self):
        """Setup the context for AES encryption tests."""
        self.key = generate_key()
        self.sample_data = "This is a test string for AES encryption."
        self.key_file_path = "aes_key.key"
        with open(self.key_file_path, "wb") as key_file:
            key_file.write(self.key)

    def tearDown(self):
        """Clean up any resources after tests."""
        if os.path.exists(self.key_file_path):
            os.remove(self.key_file_path)

    def test_generate_key(self):
        """Tests the generate_key function."""
        key = generate_key()
        self.assertIsNotNone(key, "Generated key should not be None.")
        self.assertEqual(len(key), 32, "Generated key should be 32 bytes long.")

    def test_load_key(self):
        """Tests the load_key function."""
        loaded_key = load_key(self.key_file_path)
        self.assertIsNotNone(loaded_key, "Loaded key should not be None.")
        self.assertEqual(loaded_key, self.key, "Loaded key should match the original key.")

    def test_encrypt_data(self):
        """Tests the encrypt_data function."""
        encrypted_data = encrypt_data(self.sample_data, self.key)
        self.assertIsNotNone(encrypted_data, "Encrypted data should not be None.")
        self.assertNotEqual(encrypted_data, self.sample_data, "Encrypted data should differ from the original data.")

    def test_decrypt_data(self):
        """Tests the decrypt_data function."""
        encrypted_data = encrypt_data(self.sample_data, self.key)
        decrypted_data = decrypt_data(encrypted_data, self.key)
        self.assertEqual(decrypted_data, self.sample_data, "Decrypted data should match the original data.")


if __name__ == "__main__":
    unittest.main()
