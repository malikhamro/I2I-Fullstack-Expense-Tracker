import unittest
from unittest.mock import patch, MagicMock

# Assuming the controller functions are in a module named `controllers`
from dashboard.controllers import get_migration_progress, get_migration_status

class TestControllers(unittest.TestCase):

    @patch('dashboard.controllers.some_database_module')
    def test_get_migration_progress(self, mock_db_module):
        # Setup: mocking the database call
        mock_progress_data = [{'id': 1, 'progress': 50}, {'id': 2, 'progress': 75}]
        mock_db_module.query.return_value = mock_progress_data

        # Call the function
        result = get_migration_progress()

        # Assert: ensure the function returns the data as expected
        self.assertEqual(result, mock_progress_data)
        mock_db_module.query.assert_called_once_with('SELECT * FROM migration_progress')  # Adjust the query as per actual

    @patch('dashboard.controllers.some_database_module')
    def test_get_migration_status(self, mock_db_module):
        # Setup: mocking the database call
        mock_status_data = {'status': 'in_progress'}
        mock_db_module.query.return_value = mock_status_data

        # Call the function
        result = get_migration_status()

        # Assert: ensure the function returns the data as expected
        self.assertEqual(result, mock_status_data)
        mock_db_module.query.assert_called_once_with('SELECT * FROM migration_status')   # Adjust the query as per actual

if __name__ == '__main__':
    unittest.main()
