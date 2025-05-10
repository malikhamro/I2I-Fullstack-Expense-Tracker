import unittest
from unittest.mock import patch
from permissions_management.users import assign_role, remove_role, list_user_roles

class TestUsersManagement(unittest.TestCase):

    @patch('permissions_management.users.update_user_roles_database')
    def test_assign_role(self, mock_update_user_roles_database):
        user_id = 1
        role_id = 2
        mock_update_user_roles_database.return_value = True

        result = assign_role(user_id, role_id)
        mock_update_user_roles_database.assert_called_once_with(user_id, role_id)
        self.assertTrue(result, "Role assignment did not succeed")

    @patch('permissions_management.users.update_user_roles_database')
    def test_remove_role(self, mock_update_user_roles_database):
        user_id = 1
        role_id = 2
        mock_update_user_roles_database.return_value = True

        result = remove_role(user_id, role_id)
        mock_update_user_roles_database.assert_called_once_with(user_id, role_id)
        self.assertTrue(result, "Role removal did not succeed")

    @patch('permissions_management.users.query_user_roles_database')
    def test_list_user_roles(self, mock_query_user_roles_database):
        user_id = 1
        expected_roles = ['admin', 'editor']
        mock_query_user_roles_database.return_value = expected_roles

        result = list_user_roles(user_id)
        mock_query_user_roles_database.assert_called_once_with(user_id)
        self.assertEqual(result, expected_roles, "Returned roles do not match expected roles")

if __name__ == '__main__':
    unittest.main()
