import unittest
from roles.assign_role_permissions import assign_permissions_to_role
from auth.permissions import define_permission

class TestAssignPermissionsToRole(unittest.TestCase):

    def setUp(self):
        # Setup initial data and configurations
        self.permissions = [
            {'action': 'read', 'description': 'Read access'},
            {'action': 'write', 'description': 'Write access'},
            {'action': 'delete', 'description': 'Delete access'}
        ]
        self.role = 'admin'

        # Define permissions
        for permission in self.permissions:
            define_permission(permission['action'], permission['description'])

    def test_assign_permissions_to_role(self):
        # Assign permissions to role
        assign_permissions_to_role(self.role, [perm['action'] for perm in self.permissions])

        # Function to check role validity and retrieve permissions
        from roles.check_role import check_role_validity
        retrieved_permissions = check_role_validity(self.role)

        # Validate the assigned permissions
        expected_permissions = {perm['action']: perm['description'] for perm in self.permissions}
        self.assertDictEqual(retrieved_permissions, expected_permissions)

    def test_assign_nonexistent_permission_to_role(self):
        # Try assigning a nonexistent permission to a role
        with self.assertRaises(KeyError):
            assign_permissions_to_role(self.role, ['nonexistent_permission'])

    def test_assign_permissions_to_nonexistent_role(self):
        # Try assigning permissions to a nonexistent role
        with self.assertRaises(ValueError):
            assign_permissions_to_role(None, [perm['action'] for perm in self.permissions])

if __name__ == '__main__':
    unittest.main()
