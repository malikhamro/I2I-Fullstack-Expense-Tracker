import unittest
from authentication import rbac

class TestRBAC(unittest.TestCase):

    def setUp(self):
        # Setting up roles and permissions for tests
        self.rbac_system = rbac
        self.rbac_system.initialize_roles()

    def test_initialize_roles(self):
        roles = self.rbac_system.get_all_roles()  # Assuming this function exists to retrieve all roles
        self.assertIn('admin', roles)
        self.assertIn('user', roles)
        self.assertIn('guest', roles)
        
        # Check if permissions are correctly assigned
        admin_permissions = self.rbac_system.get_permissions('admin')  # Assuming this function exists to retrieve permissions for a role
        user_permissions = self.rbac_system.get_permissions('user')
        guest_permissions = self.rbac_system.get_permissions('guest')
        
        self.assertTrue('write' in admin_permissions)
        self.assertTrue('read' in admin_permissions)
        self.assertTrue('read' in user_permissions)
        self.assertFalse('write' in user_permissions)
        self.assertTrue('read' in guest_permissions)
        self.assertFalse('write' in guest_permissions)

    def test_assign_role(self):
        user_id = 1
        role = 'user'
        self.rbac_system.assign_role(user_id, role)
        roles = self.rbac_system.get_user_roles(user_id)  # Assuming this function exists to retrieve roles for a user
        self.assertIn(role, roles)
        
    def test_check_permission(self):
        user_id = 1
        self.rbac_system.assign_role(user_id, 'user')
        self.assertTrue(self.rbac_system.check_permission(user_id, 'read'))
        self.assertFalse(self.rbac_system.check_permission(user_id, 'write'))
        
        self.rbac_system.assign_role(user_id, 'admin')
        self.assertTrue(self.rbac_system.check_permission(user_id, 'write'))

    def test_revoke_role(self):
        user_id = 1
        role = 'user'
        self.rbac_system.assign_role(user_id, role)
        self.rbac_system.revoke_role(user_id, role)
        roles = self.rbac_system.get_user_roles(user_id)
        self.assertNotIn(role, roles)

if __name__ == '__main__':
    unittest.main()
