import unittest
from unittest.mock import patch, MagicMock

# Import the function to be tested
from src.update_claim_status import update_claim_status

class TestUpdateClaimStatus(unittest.TestCase):

    @patch('src.database.update_claim_status_in_db')
    @patch('src.notifications.notify_stakeholders')
    @patch('src.database.get_claim_by_id')
    def test_update_claim_status_success(self, mock_get_claim, mock_notify, mock_update_db):
        # Setting up mock return values
        claim_id = 123
        new_status = 'Approved'
        remarks = 'Valid claim, approved'
        
        mock_get_claim.return_value = {'claim_id': claim_id, 'status': 'Pending'}
        mock_update_db.return_value = True
        mock_notify.return_value = True

        # Call the function
        result = update_claim_status(claim_id, new_status, remarks)

        # Assertions to check if the function behaves as expected
        self.assertTrue(result)
        mock_get_claim.assert_called_once_with(claim_id)
        mock_update_db.assert_called_once_with(claim_id, new_status)
        mock_notify.assert_called_once()

    @patch('src.database.update_claim_status_in_db')
    @patch('src.notifications.notify_stakeholders')
    @patch('src.database.get_claim_by_id')
    def test_update_claim_status_failure(self, mock_get_claim, mock_notify, mock_update_db):
        # Scenario: Invalid claim ID
        claim_id = 999
        new_status = 'Approved'
        remarks = 'Valid claim, approved'
        
        mock_get_claim.return_value = None

        # Call the function
        result = update_claim_status(claim_id, new_status, remarks)

        # Assertions to check if the function handles invalid claim ID
        self.assertFalse(result)
        mock_get_claim.assert_called_once_with(claim_id)
        mock_update_db.assert_not_called()
        mock_notify.assert_not_called()

        # Scenario: Database update failure
        claim_id = 123
        mock_get_claim.return_value = {'claim_id': claim_id, 'status': 'Pending'}
        mock_update_db.return_value = False

        # Call the function
        result = update_claim_status(claim_id, new_status, remarks)

        # Assertions to check if the function handles database update failure
        self.assertFalse(result)
        mock_get_claim.assert_called_with(claim_id)
        mock_update_db.assert_called_once_with(claim_id, new_status)
        mock_notify.assert_not_called()

if __name__ == '__main__':
    unittest.main()
