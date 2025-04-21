import unittest
from unittest.mock import patch, mock_open
from config_changes.config_logger import log_changes

class TestConfigLogger(unittest.TestCase):

    @patch('config_changes.config_logger.open', new_callable=mock_open)
    @patch('config_changes.config_logger.os.path.exists')
    def test_log_changes(self, mock_exists, mock_open):
        # Set up
        mock_exists.return_value = True
        change_details = {
            'user': 'admin',
            'timestamp': '2023-10-10 10:00:00',
            'config_parameter': 'max_connections',
            'old_value': '100',
            'new_value': '200'
        }
        
        # Call the function under test
        log_changes(change_details)
        
        # Assertions to confirm the changes are logged correctly
        mock_open.assert_called_once_with('config_changes.log', 'a')
        file_handle = mock_open()
        file_handle.write.assert_any_call('User: admin\n')
        file_handle.write.assert_any_call('Timestamp: 2023-10-10 10:00:00\n')
        file_handle.write.assert_any_call('Changed Config: max_connections\n')
        file_handle.write.assert_any_call('Old Value: 100\n')
        file_handle.write.assert_any_call('New Value: 200\n')
        file_handle.write.assert_any_call('-'*40 + '\n')

    @patch('config_changes.config_logger.open', new_callable=mock_open)
    @patch('config_changes.config_logger.os.path.exists')
    def test_log_changes_file_creation(self, mock_exists, mock_open):
        # Set up
        mock_exists.return_value = False
        change_details = {
            'user': 'admin',
            'timestamp': '2023-10-10 10:00:00',
            'config_parameter': 'max_connections',
            'old_value': '100',
            'new_value': '200'
        }
        
        # Call the function under test
        log_changes(change_details)
        
        # Assertions to confirm the log file is created and written correctly
        mock_open.assert_called_once_with('config_changes.log', 'w')
        file_handle = mock_open()
        file_handle.write.assert_any_call('User: admin\n')
        file_handle.write.assert_any_call('Timestamp: 2023-10-10 10:00:00\n')
        file_handle.write.assert_any_call('Changed Config: max_connections\n')
        file_handle.write.assert_any_call('Old Value: 100\n')
        file_handle.write.assert_any_call('New Value: 200\n')
        file_handle.write.assert_any_call('-'*40 + '\n')

    def test_log_changes_invalid_data(self):
        # Test with missing fields in change_details
        change_details = {
            'user': 'admin',
            'timestamp': '2023-10-10 10:00:00',
            # Missing 'config_parameter', 'old_value' and 'new_value'
        }
        
        with self.assertRaises(KeyError):
            log_changes(change_details)

if __name__ == '__main__':
    unittest.main()

