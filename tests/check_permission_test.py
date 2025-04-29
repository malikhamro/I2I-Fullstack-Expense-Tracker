import unittest
from unittest.mock import patch
from auth.check_permission import check_user_permission

class TestCheckUserPermission(unittest.TestCase):
    
    @patch('auth.check_permission.define_permission')
    def test_check_user_permission_define_permission(self, mock_define_permission):
        # Set up the mock permissions returned by define_permission
        mock_define_permission.return_value = {
            'view_dashboard': 'Allows viewing of the dashboard',
            'edit_profile': 'Allows editing of user profile'
        }
        
        # Test cases with the expected results
        test_cases = [
            {'user_roles_permissions': ['view_dashboard'], 'action': 'view_dashboard', 'expected': True},
            {'user_roles_permissions': ['edit_profile'], 'action': 'view_dashboard', 'expected': False},
            {'user_roles_permissions': [], 'action': 'edit_profile', 'expected': False},
            {'user_roles_permissions': ['edit_profile', 'view_dashboard'], 'action': 'edit_profile', 'expected': True},
        ]
        
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                user_roles_permissions = test_case['user_roles_permissions']
                action = test_case['action']
                expected = test_case['expected']
                
                # Call the function and check the result
                result = check_user_permission(user_roles_permissions, action)
                self.assertEqual(result, expected, f"Failed for user permissions: {user_roles_permissions}, action: {action}")

if __name__ == '__main__':
    unittest.main()
