import unittest
from backup_service.config import get_backup_settings, get_recovery_settings

class TestConfig(unittest.TestCase):
    
    def setUp(self):
        # Mocking the configuration settings which should be retrieved from a config file or environment variables.
        self.expected_backup_settings = {
            'frequency': 'daily',
            'storage_location': '/backups/',
            'retention_period': '30 days'
        }
        self.expected_recovery_settings = {
            'retry_attempts': 3,
            'retry_interval': '5 minutes'
        }
        
    def test_get_backup_settings(self):
        backup_settings = get_backup_settings()
        self.assertEqual(backup_settings['frequency'], self.expected_backup_settings['frequency'])
        self.assertEqual(backup_settings['storage_location'], self.expected_backup_settings['storage_location'])
        self.assertEqual(backup_settings['retention_period'], self.expected_backup_settings['retention_period'])
    
    def test_get_recovery_settings(self):
        recovery_settings = get_recovery_settings()
        self.assertEqual(recovery_settings['retry_attempts'], self.expected_recovery_settings['retry_attempts'])
        self.assertEqual(recovery_settings['retry_interval'], self.expected_recovery_settings['retry_interval'])

if __name__ == '__main__':
    unittest.main()
