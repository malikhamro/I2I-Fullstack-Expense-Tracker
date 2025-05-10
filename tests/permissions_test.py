import unittest
from auth.permissions import define_permission
import os

class TestDefinePermission(unittest.TestCase):
    
    def setUp(self):
        # Set up a mock database or configuration file for testing
        self.permissions_file = 'test_permissions.json'
        if os.path.exists(self.permissions_file):
            os.remove(self.permissions_file)

    def tearDown(self):
        # Clean up the mock database or configuration file after each test
        if os.path.exists(self.permissions_file):
            os.remove(self.permissions_file)

    def test_define_permission_valid(self):
        # Test defining a valid permission
        action_name = 'edit_article'
        description = 'Permission to edit an article'
        
        result = define_permission(action_name, description, self.permissions_file)
        self.assertTrue(result)
        
        # Verify the permission is stored correctly
        with open(self.permissions_file, 'r') as file:
            permissions = json.load(file)
        
        self.assertIn(action_name, permissions)
        self.assertEqual(permissions[action_name], description)

    def test_define_permission_invalid_empty_action_name(self):
        # Test defining a permission with an empty action name
        action_name = ''
        description = 'Permission to edit an article'
        
        result = define_permission(action_name, description, self.permissions_file)
        self.assertFalse(result)
        
        # Verify no permission is stored
        with open(self.permissions_file, 'r') as file:
            permissions = json.load(file)
        
        self.assertNotIn(action_name, permissions)

    def test_define_permission_invalid_empty_description(self):
        # Test defining a permission with an empty description
        action_name = 'edit_article'
        description = ''
        
        result = define_permission(action_name, description, self.permissions_file)
        self.assertFalse(result)
        
        # Verify no permission is stored
        with open(self.permissions_file, 'r') as file:
            permissions = json.load(file)
        
        self.assertNotIn(action_name, permissions)

    def test_define_permission_duplicate(self):
        # Test defining a duplicate permission
        action_name = 'edit_article'
        description = 'Permission to edit an article'

        _ = define_permission(action_name, description, self.permissions_file)
        
        duplicate_result = define_permission(action_name, description, self.permissions_file)
        self.assertFalse(duplicate_result)
        
        # Verify only one permission is stored
        with open(self.permissions_file, 'r') as file:
            permissions = json.load(file)
        
        self.assertEqual(len(permissions), 1)
        self.assertIn(action_name, permissions)
        self.assertEqual(permissions[action_name], description)

if __name__ == '__main__':
    unittest.main()
