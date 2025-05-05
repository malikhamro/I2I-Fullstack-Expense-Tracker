import unittest
from permissions_management.permissions import add_permission, remove_permission, list_permissions
from permissions_management.db import PermissionsDatabase  # Assuming a module for DB operations

class TestPermissionsManagement(unittest.TestCase):

    def setUp(self):
        # This method will run before each test
        self.db = PermissionsDatabase()
        self.role_id = 1
        self.permission = "read-only"

        # Adding test role and permission details to the DB
        self.db.create_role(self.role_id)  
        self.db.add_permission(self.role_id, "write")

    def tearDown(self):
        # This method will run after each test
        self.db.remove_role(self.role_id)

    def test_add_permission(self):
        # Testing the add_permission function
        add_permission(self.role_id, self.permission)
        permissions = list_permissions(self.role_id)
        self.assertIn(self.permission, permissions, f"Permission {self.permission} was not added successfully.")

    def test_remove_permission(self):
        # Adding a permission to be removed for testing
        self.db.add_permission(self.role_id, self.permission)
        
        # Testing the remove_permission function
        remove_permission(self.role_id, self.permission)
        permissions = list_permissions(self.role_id)
        self.assertNotIn(self.permission, permissions, f"Permission {self.permission} was not removed successfully.")

    def test_list_permissions(self):
        # Adding multiple permissions for testing
        self.db.add_permission(self.role_id, self.permission)
        self.db.add_permission(self.role_id, "delete")

        # Testing the list_permissions function
        permissions = list_permissions(self.role_id)
        expected_permissions = {"write", "read-only", "delete"}
        
        self.assertEqual(set(permissions), expected_permissions, "The listed permissions do not match expected permissions.")
        
if __name__ == '__main__':
    unittest.main()
