import unittest
from unittest.mock import patch
from users.check_user_role import verify_user_role

class TestVerifyUserRole(unittest.TestCase):
    
    @patch('roles.check_role.check_role_validity')
    def test_verify_user_role(self, mock_check_role_validity):
        # Mocking the return value of check_role_validity
        mock_check_role_validity.return_value = {
            "role_exists": True,
            "permissions": ["read", "write"]
        }
        
        # Define the test data
        user_id = 1
        expected_role = "admin"
        expected_permissions = ["read", "write"]
        
        with patch('users.check_user_role.get_user_role') as mock_get_user_role:
            # Mocking the return value of get_user_role
            mock_get_user_role.return_value = expected_role
            
            # Run the function and capture the output
            result = verify_user_role(user_id)
            
            # Validate the results
            self.assertEqual(result["role"], expected_role)
            self.assertEqual(result["permissions"], expected_permissions)
            mock_get_user_role.assert_called_once_with(user_id)
            mock_check_role_validity.assert_called_once_with(expected_role)

    @patch('roles.check_role.check_role_validity')
    def test_verify_user_role_invalid_role(self, mock_check_role_validity):
        # Mocking the return value of check_role_validity for invalid role
        mock_check_role_validity.return_value = {
            "role_exists": False,
            "permissions": []
        }
        
        # Define the test data
        user_id = 2
        expected_role = "nonexistent"
        
        with patch('users.check_user_role.get_user_role') as mock_get_user_role:
            # Mocking the return value of get_user_role
            mock_get_user_role.return_value = expected_role
            
            # Run the function and capture the output
            result = verify_user_role(user_id)
            
            # Validate the results
            self.assertEqual(result["role"], expected_role)
            self.assertEqual(result["permissions"], [])
            mock_get_user_role.assert_called_once_with(user_id)
            mock_check_role_validity.assert_called_once_with(expected_role)

    @patch('roles.check_role.check_role_validity')
    def test_verify_user_role_no_role(self, mock_check_role_validity):
        # Mocking the return value of check_role_validity for no role assigned
        mock_check_role_validity.return_value = {
            "role_exists": False,
            "permissions": []
        }
        
        # Define the test data
        user_id = 3
        expected_role = None
        
        with patch('users.check_user_role.get_user_role') as mock_get_user_role:
            # Mocking the return value of get_user_role
            mock_get_user_role.return_value = expected_role
            
            # Run the function and capture the output
            result = verify_user_role(user_id)
            
            # Validate the results
            self.assertEqual(result["role"], expected_role)
            self.assertEqual(result["permissions"], [])
            mock_get_user_role.assert_called_once_with(user_id)
            mock_check_role_validity.assert_called_once_with(expected_role)

if __name__ == '__main__':
    unittest.main()
