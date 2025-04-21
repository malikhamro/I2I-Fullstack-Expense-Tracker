import unittest
from unittest.mock import patch, call
from observer import watch_config_changes
from change_notifier import send_notification


class TestObserver(unittest.TestCase):
    
    @patch('observer.watch_config_changes')
    @patch('change_notifier.send_notification')
    def test_watch_config_changes(self, mock_send_notification, mock_watch_config_changes):
        # Simulate a configuration change
        mock_watch_config_changes.return_value = True
        
        # Call the function to test
        watch_config_changes()
        
        # Ensure the watch_config_changes function was called
        mock_watch_config_changes.assert_called_once()
        
        # Ensure the send_notification function was triggered upon detecting a change
        mock_send_notification.assert_called_once_with("Configuration change detected")
        
        # Simulate no configuration change
        mock_watch_config_changes.return_value = False
        
        # Call the function to test
        watch_config_changes()
        
        # Ensure the send_notification function was not called again since there was no change
        self.assertEqual(mock_send_notification.call_count, 1)


if __name__ == '__main__':
    unittest.main()
