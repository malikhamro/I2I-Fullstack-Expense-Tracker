import unittest
from unittest.mock import patch, MagicMock
from src.notifications import notify_stakeholders

class TestNotifications(unittest.TestCase):

    @patch('src.notifications.notify_stakeholders')
    def test_notify_stakeholders(self, mock_notify_stakeholders):
        # Create mock parameters
        claim_details = {
            'claim_id': '12345',
            'policy_holder': 'John Doe',
            'insured_amount': 10000.00,
            'status': 'Approved'
        }
        new_status = 'Approved'
        remarks = 'Verified and approved'

        # Call the function
        notify_stakeholders(claim_details, new_status, remarks)

        # Assert the notification function is called with correct parameters
        mock_notify_stakeholders.assert_called_with(claim_details, new_status, remarks)
        
        # Validate additional behaviors if any
        self.assertTrue(mock_notify_stakeholders.called)

    def test_notify_stakeholders_failure(self):
        claim_details = None  # Simulating failure scenario with None claim_details
        new_status = 'Approved'
        remarks = 'Verified and approved'

        with self.assertRaises(TypeError):  # Expecting TypeError for invalid input (None)
            notify_stakeholders(claim_details, new_status, remarks)

if __name__ == '__main__':
    unittest.main()
