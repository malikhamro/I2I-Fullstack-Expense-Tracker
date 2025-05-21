import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import logging.modification_logger as mod_log


class TestModificationLogger(unittest.TestCase):
    @patch('logging.modification_logger.datetime')
    @patch('logging.modification_logger.open')
    def test_log_modification_creation(self, mock_open, mock_datetime):
        # Setup the mock objects
        mock_datetime.now.return_value = datetime(2023, 10, 21, 12, 0, 0)
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Test data
        user_id = "user123"
        modified_fields = {
            "name": ("Old Name", "New Name"),
            "age": (30, 31)
        }
        
        # Call the function
        mod_log.log_modification(user_id, modified_fields)
        
        # Expected log entry
        expected_log_entry = (
            "2023-10-21T12:00:00 - User ID: user123 modified fields:\n"
            "  name: Old Value='Old Name', New Value='New Name'\n"
            "  age: Old Value=30, New Value=31\n"
        )
        
        # Assertions to ensure proper logging
        mock_open.assert_called_once_with('modification_logs.txt', 'a')
        mock_file.write.assert_called_once_with(expected_log_entry)


if __name__ == '__main__':
    unittest.main()
