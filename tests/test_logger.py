import unittest
from unittest.mock import patch, mock_open, MagicMock
import logging

# Assuming that logger functions are located in 'backup_service/logger.py'
from backup_service.logger import log_backup_activity, log_recovery_activity

class TestLogger(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('backup_service.logger.logging.getLogger')
    def test_log_backup_activity(self, mock_getLogger, mock_open):
        # Mocking logger
        mock_logger = MagicMock()
        mock_getLogger.return_value = mock_logger
        
        # Test data
        activity = {
            "time": "2023-10-12 10:00:00",
            "data_size": "50MB",
            "status": "Success"
        }
        
        # Call the function to test
        log_backup_activity(activity)
        
        # Validate logger calls
        mock_logger.info.assert_called_with(f"Backup Activity - Time: {activity['time']}, Data Size: {activity['data_size']}, Status: {activity['status']}")

    @patch('builtins.open', new_callable=mock_open)
    @patch('backup_service.logger.logging.getLogger')
    def test_log_recovery_activity(self, mock_getLogger, mock_open):
        # Mocking logger
        mock_logger = MagicMock()
        mock_getLogger.return_value = mock_logger
        
        # Test data
        activity = {
            "time": "2023-10-12 11:00:00",
            "status": "Success",
            "errors": None
        }
        
        # Call the function to test
        log_recovery_activity(activity)
        
        # Validate logger calls
        mock_logger.info.assert_called_with(f"Recovery Activity - Time: {activity['time']}, Status: {activity['status']}, Errors: {activity['errors']}")

if __name__ == '__main__':
    unittest.main()
