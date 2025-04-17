import unittest
from utils.data_fetcher import fetch_migration_data

class TestDataFetcher(unittest.TestCase):

    def setUp(self):
        # Set up any necessary initial states or variables
        self.expected_data = [
            {"id": 1, "status": "completed", "details": "Migration of user data"},
            {"id": 2, "status": "in-progress", "details": "Migration of transaction data"}
        ]
        self.source_database = "test_source_db"

    def test_fetch_migration_data(self):
        # Test if fetch_migration_data correctly fetches data from the source database
        try:
            result = fetch_migration_data(self.source_database)
            self.assertIsNotNone(result, "Fetched data should not be None.")
            self.assertIsInstance(result, list, "Fetched data should be a list.")
            self.assertListEqual(result, self.expected_data, "Fetched data does not match the expected data.")
        except Exception as e:
            self.fail(f"An error occurred: {e}")

    def test_fetch_migration_data_empty_database(self):
        # Test fetching data from an empty database
        empty_database = "empty_db"
        result = fetch_migration_data(empty_database)
        self.assertIsInstance(result, list, "Result should be a list.")
        self.assertEqual(len(result), 0, "Result should be an empty list for an empty database.")

    def test_fetch_migration_data_invalid_database(self):
        # Test fetching data from an invalid database
        invalid_database = "invalid_db"
        with self.assertRaises(ValueError, msg="Should raise ValueError for invalid databases"):
            fetch_migration_data(invalid_database)

if __name__ == "__main__":
    unittest.main()
