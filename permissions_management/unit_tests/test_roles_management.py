import unittest
from permissions_management.roles import create_role, delete_role, list_roles

class TestRolesManagement(unittest.TestCase):
    
    def setUp(self):
        # Set up any preconditions here.
        # This might include initializing test databases or mock objects.
        self.test_role_name = "test_role"
        self.test_role_id = 1
        # Assuming there's a mock or in-memory database initialized here
        # Example: self.mock_db = MockDatabase()
    
    def tearDown(self):
        # Clean up any resources allocated in setUp here.
        # Example: self.mock_db.cleanup()
        pass

    def test_create_role(self):
        """
        Unit test to verify that the create_role function correctly creates a new role.
        """
        # Call create_role and verify if the role is created.
        result = create_role(self.test_role_name)
        
        # Verify the results
        self.assertIsNotNone(result)
        self.assertEqual(result['role_name'], self.test_role_name)
        self.assertIn('role_id', result)  # Assuming role_id is given upon creation:
        self.test_role_id = result['role_id']

    def test_delete_role(self):
        """
        Unit test to verify that the delete_role function correctly deletes the specified role.
        """
        # Assuming the role needs to exist before attempting deletion
        create_role(self.test_role_name)
        
        # Call delete_role and verify if the role is deleted.
        result = delete_role(self.test_role_id)
        
        # Verify the results
        self.assertTrue(result)
        # Also verify the role has been removed:
        roles = list_roles()
        self.assertNotIn(self.test_role_id, [role['role_id'] for role in roles])

    def test_list_roles(self):
        """
        Unit test to verify that the list_roles function displays all existing roles in the system.
        """
        # First ensure there is at least one role by creating one
        create_role(self.test_role_name)
        
        # Call list_roles and verify if the roles are listed.
        roles = list_roles()
        
        # Verify the results
        self.assertIsInstance(roles, list)
        self.assertGreater(len(roles), 0)
        self.assertIn(self.test_role_name, [role['role_name'] for role in roles])

if __name__ == '__main__':
    unittest.main()
