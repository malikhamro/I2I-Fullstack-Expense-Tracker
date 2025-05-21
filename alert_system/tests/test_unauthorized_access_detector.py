import unittest
from unittest.mock import patch, MagicMock
from alert_system.detector.unauthorized_access_detector import detect_unauthorized_access
from alert_system.alerter.alert_sender import send_alert

class TestUnauthorizedAccessDetector(unittest.TestCase):

    @patch('alert_system.detector.unauthorized_access_detector.detect_unauthorized_access')
    @patch('alert_system.alerter.alert_sender.send_alert')
    def test_detect_unauthorized_access(self, mock_send_alert, mock_detect_unauthorized_access):
        # Mock the real-time access log data for the test case
        mock_access_log = [
            {'timestamp': '2023-10-01 10:00:00', 'user_id': 'user123', 'status': 'SUCCESS'},
            {'timestamp': '2023-10-01 10:05:00', 'user_id': 'intruder', 'status': 'FAILURE'},
            {'timestamp': '2023-10-01 10:10:00', 'user_id': 'user456', 'status': 'SUCCESS'},
        ]

        # Configure the mock behavior
        mock_detect_unauthorized_access.return_value = [attempt for attempt in mock_access_log if attempt['status'] == 'FAILURE']
        
        # Call the function to test
        unauthorized_attempts = detect_unauthorized_access(mock_access_log)
        
        # Assert that unauthorized attempts are detected correctly
        self.assertEqual(len(unauthorized_attempts), 1)
        self.assertEqual(unauthorized_attempts[0]['user_id'], 'intruder')

        # Check if send_alert is triggered for unauthorized access attempt
        mock_send_alert.assert_called_once_with(unauthorized_attempts[0])

if __name__ == '__main__':
    unittest.main()
