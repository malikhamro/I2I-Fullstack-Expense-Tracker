import unittest
from unittest.mock import patch, MagicMock
from utils.data_updater import update_dashboard_data  # We're assuming this function exists in the utils/data_updater.py module

class TestDataUpdater(unittest.TestCase):
    @patch('utils.data_updater.fetch_migration_data')
    @patch('utils.data_updater.analyze_migration_data')
    @patch('utils.data_updater.ui_elements')  # Let's assume the function interacts with UI elements
    def test_update_dashboard_data(self, mock_ui_elements, mock_analyze_migration_data, mock_fetch_migration_data):
        # Arrange: Setting up mock return values and expected outcomes
        mock_fetch_migration_data.return_value = {'data': 'sample migration data'}
        mock_analyze_migration_data.return_value = {'status': 'complete', 'progress': '100%'}
        
        dashboard_mock = MagicMock()
        dashboard_mock.update_status = MagicMock()
        dashboard_mock.update_progress = MagicMock()
        
        mock_ui_elements.return_value = dashboard_mock
        
        # Act: Call the function under test
        update_dashboard_data()
        
        # Assert: Validate that the dashboard is updated with correct data
        dashboard_mock.update_status.assert_called_once_with('complete')
        dashboard_mock.update_progress.assert_called_once_with('100%')

        # Verify interaction with analyze_migration_data
        mock_analyze_migration_data.assert_called_once_with({'data': 'sample migration data'})
        
        # Verify interaction with fetch_migration_data
        mock_fetch_migration_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()
