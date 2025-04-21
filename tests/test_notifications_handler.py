import unittest
from unittest.mock import patch
from notifications.notifications_handler import send_email_notification, send_sms_notification, send_push_notification

class TestNotificationsHandler(unittest.TestCase):

    @patch('notifications.notifications_handler.smtplib.SMTP')
    def test_send_email_notification(self, mock_smtp):
        # Mocking the SMTP server response
        instance = mock_smtp.return_value
        instance.sendmail.return_value = {}

        result = send_email_notification('admin@example.com', 'Configuration Change', 'A change has occurred.')

        instance.sendmail.assert_called_with(
            'from@example.com',
            'admin@example.com',
            'Subject: Configuration Change\n\nA change has occurred.'
        )
        self.assertTrue(result)

    @patch('notifications.notifications_handler.twilio.Client')
    def test_send_sms_notification(self, mock_twilio_client):
        # Mocking the Twilio client response
        instance = mock_twilio_client.return_value
        instance.messages.create.return_value = 'SM12345'

        result = send_sms_notification('+1234567890', 'A change has occurred.')

        instance.messages.create.assert_called_with(
            body='A change has occurred.',
            from_='+1987654321',
            to='+1234567890'
        )
        self.assertEqual(result, 'SM12345')
    
    @patch('notifications.notifications_handler.push_service.send_notification')
    def test_send_push_notification(self, mock_send_notification):
        # Mocking the push notification response
        mock_send_notification.return_value = True

        result = send_push_notification('A change has occurred.')

        mock_send_notification.assert_called_once_with('A change has occurred.')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
