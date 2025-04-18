import unittest
from unittest.mock import patch, MagicMock
from notifications.change_notifier import send_notification

class TestChangeNotifier(unittest.TestCase):
    
    @patch('notifications.change_notifier.send_notification')
    def test_send_notification(self, mock_send_notification):
        # Arrange
        change_details = {
            'config_name': 'max_connections',
            'old_value': '100',
            'new_value': '200'
        }
        expected_message = (
            "Configuration Change Alert:\n\n"
            "The configuration 'max_connections' has been changed.\n"
            "Old Value: 100\n"
            "New Value: 200\n"
        )

        # Act
        send_notification(change_details)
        
        # Assert
        mock_send_notification.assert_called_once_with(change_details)
        # Assuming send_notification sends the message to an external system,
        # we are verifying that the function is called correctly with formatted message.
        actual_message = mock_send_notification.call_args[0][0]
        self.assertEqual(
            f"Configuration Change Alert:\n\n"
            f"The configuration '{change_details['config_name']}' has been changed.\n"
            f"Old Value: {change_details['old_value']}\n"
            f"New Value: {change_details['new_value']}\n",
            expected_message
        )

if __name__ == '__main__':
    unittest.main()
