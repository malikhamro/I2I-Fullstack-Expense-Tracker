import unittest
from unittest.mock import patch
from services.user_service import get_user_roles

class TestUserService(unittest.TestCase):
    
    @patch('services.user_service.get_user_roles')
    def test_get_user_roles(self, mock_get_user_roles):
        # Test data setup
        user_id = 1
        expected_roles = ['admin', 'user']
        
        # Configure the mock to return the expected roles
        mock_get_user_roles.return_value = expected_roles
        
        # Call the function under test
        roles = get_user_roles(user_id)
        
        # Assertions to ensure the function returns the correct roles
        self.assertEqual(roles, expected_roles)
        mock_get_user_roles.assert_called_once_with(user_id)
        mock_get_user_roles.assert_called_with(user_id)

if __name__ == '__main__':
    unittest.main()
