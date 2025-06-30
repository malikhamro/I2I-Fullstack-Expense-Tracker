import unittest
from unittest.mock import patch
from data_consistency.notifications import send_alert, notify_policy_update

class TestNotifications(unittest.TestCase):
    
    @patch('data_consistency.notifications.send_alert')
    def test_send_alert(self, mock_send_alert):
        # Arrange
        mock_send_alert.return_value = True
        message = "Inconsistency detected in service XYZ"
        
        # Act
        result = send_alert(message)
        
        # Assert
        mock_send_alert.assert_called_once_with(message)
        self.assertTrue(result)

    @patch('data_consistency.notifications.notify_policy_update')
    def test_notify_policy_update(self, mock_notify_policy_update):
        # Arrange
        mock_notify_policy_update.return_value = True
        policy_details = {"policy_id": 1, "update": "New policy updates"}
        
        # Act
        result = notify_policy_update(policy_details)
        
        # Assert
        mock_notify_policy_update.assert_called_once_with(policy_details)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
