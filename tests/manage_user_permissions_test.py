import unittest
from unittest.mock import patch, MagicMock
from users.manage_user_permissions import assign_permissions_to_user

class TestAssignPermissionsToUser(unittest.TestCase):
    @patch('users.manage_user_permissions.get_user_by_id')
    @patch('users.manage_user_permissions.get_permissions_by_role')
    def test_assign_permissions_to_user(self, mock_get_permissions_by_role, mock_get_user_by_id):
        # Setup mocks
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.permissions = []

        mock_get_user_by_id.return_value = mock_user
        mock_get_permissions_by_role.return_value = ['read', 'write']

        # Specific permissions to assign to the user, overriding role-based permissions
        specific_permissions = ['delete', 'create']

        # Call to function under test
        updated_user = assign_permissions_to_user(mock_user.id, specific_permissions)

        # Assertions
        self.assertEqual(updated_user.permissions, ['delete', 'create'])

        mock_get_user_by_id.assert_called_once_with(mock_user.id)
        mock_get_permissions_by_role.assert_not_called()

    @patch('users.manage_user_permissions.get_user_by_id')
    @patch('users.manage_user_permissions.get_permissions_by_role')
    @patch('users.manage_user_permissions.save_user_permissions')
    def test_assign_permissions_to_user_with_role_permissions(self, mock_save_user_permissions, mock_get_permissions_by_role, mock_get_user_by_id):
        # Setup mocks
        mock_user = MagicMock()
        mock_user.id = 2
        mock_user.permissions = []

        mock_get_user_by_id.return_value = mock_user
        mock_get_permissions_by_role.return_value = ['read', 'write']

        # Specific permissions left as None, meaning role-based permissions should be used
        specific_permissions = None

        # Call to function under test
        updated_user = assign_permissions_to_user(mock_user.id, specific_permissions)

        # Assertions
        self.assertEqual(updated_user.permissions, ['read', 'write'])
        
        mock_get_user_by_id.assert_called_once_with(mock_user.id)
        mock_get_permissions_by_role.assert_called_once_with(mock_user.id)
        mock_save_user_permissions.assert_called_once_with(mock_user)

    @patch('users.manage_user_permissions.get_user_by_id')
    @patch('users.manage_user_permissions.get_permissions_by_role')
    def test_assign_permissions_to_user_with_empty_specific_permissions(self, mock_get_permissions_by_role, mock_get_user_by_id):
        # Setup mocks
        mock_user = MagicMock()
        mock_user.id = 3
        mock_user.permissions = []

        mock_get_user_by_id.return_value = mock_user
        mock_get_permissions_by_role.return_value = ['read']

        # Specific permissions is an empty list, should override role-based permissions with empty list
        specific_permissions = []

        # Call to function under test
        updated_user = assign_permissions_to_user(mock_user.id, specific_permissions)

        # Assertions
        self.assertEqual(updated_user.permissions, [])

        mock_get_user_by_id.assert_called_once_with(mock_user.id)
        mock_get_permissions_by_role.assert_not_called()

if __name__ == '__main__':
    unittest.main()
