import unittest
from unittest.mock import patch, MagicMock
from dashboard.services.data_service import fetch_migration_data, aggregate_migration_data

class TestDataService(unittest.TestCase):

    @patch('dashboard.services.data_service.db_connection')
    def test_fetch_migration_data(self, mock_db_connection):
        # Set up the mock database connection and cursor
        mock_cursor = MagicMock()
        mock_db_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'id': 1, 'name': 'Sample Migration Data'}
        
        # Call the function
        result = fetch_migration_data()

        # Assertions to ensure the function retrieves data correctly
        self.assertIsNotNone(result)
        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['name'], 'Sample Migration Data')
        
        # Ensure the cursor and connection were used correctly
        mock_db_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM migration_data LIMIT 1')
        mock_cursor.fetchone.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db_connection.close.assert_called_once()

    def test_aggregate_migration_data(self):
        # Example raw migration data for testing
        raw_data = [
            {'status': 'completed', 'count': 5},
            {'status': 'in_progress', 'count': 3},
            {'status': 'failed', 'count': 2}
        ]

        # Expected result after aggregation
        expected_result = {
            'total_migrations': 10,
            'completed': 5,
            'in_progress': 3,
            'failed': 2
        }

        # Call the function
        result = aggregate_migration_data(raw_data)

        # Assertions to ensure the function processes data correctly
        self.assertEqual(result['total_migrations'], expected_result['total_migrations'])
        self.assertEqual(result['completed'], expected_result['completed'])
        self.assertEqual(result['in_progress'], expected_result['in_progress'])
        self.assertEqual(result['failed'], expected_result['failed'])

if __name__ == '__main__':
    unittest.main()
