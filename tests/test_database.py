import unittest
from unittest.mock import patch
from src.database import update_claim_status_in_db, get_claim_by_id

class TestDatabase(unittest.TestCase):

    @patch('src.database.update_claim_status_in_db')
    def test_update_claim_status_in_db(self, mock_update):
        # Setup
        claim_id = 12345
        new_status = 'approved'
        
        # Act
        update_claim_status_in_db(claim_id, new_status)
        
        # Assert
        mock_update.assert_called_with(claim_id, new_status)

    @patch('src.database.get_claim_by_id')
    def test_get_claim_by_id(self, mock_get_claim):
        # Setup
        claim_id = 12345
        expected_claim = {
            'id': claim_id,
            'status': 'pending',
            'remarks': 'Initial claim'
        }
        mock_get_claim.return_value = expected_claim
        
        # Act
        actual_claim = get_claim_by_id(claim_id)
        
        # Assert
        self.assertEqual(actual_claim, expected_claim)
        mock_get_claim.assert_called_with(claim_id)

# Run the tests
if __name__ == '__main__':
    unittest.main()
