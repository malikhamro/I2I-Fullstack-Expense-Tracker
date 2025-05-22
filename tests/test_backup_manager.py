import unittest
from unittest.mock import patch, MagicMock
from backup_service.backup_manager import perform_backup, schedule_backups
from backup_service.config import get_backup_settings
from backup_service.logger import log_backup_activity

class TestBackupManager(unittest.TestCase):

    @patch('backup_service.backup_manager.perform_backup')
    @patch('backup_service.logger.log_backup_activity')
    def test_perform_backup(self, mock_log_backup_activity, mock_perform_backup):
        # Arrange
        mock_perform_backup.return_value = True
        backup_data = 'sample_backup_data'
        
        # Act
        result = perform_backup()

        # Assert
        self.assertTrue(result)
        mock_perform_backup.assert_called_once()
        mock_log_backup_activity.assert_called_once_with({'status': 'success', 'data': backup_data})

    @patch('backup_service.backup_manager.schedule_backups')
    @patch('backup_service.config.get_backup_settings')
    def test_schedule_backups(self, mock_get_backup_settings, mock_schedule_backups):
        # Arrange
        mock_get_backup_settings.return_value = {'frequency': 'daily'}
        mock_schedule_backups.return_value = True

        # Act
        result = schedule_backups()

        # Assert
        self.assertTrue(result)
        mock_schedule_backups.assert_called_once()
        mock_get_backup_settings.assert_called_once()

if __name__ == '__main__':
    unittest.main()
