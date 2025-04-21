import unittest
from unittest.mock import patch, MagicMock
from services.resource_service import access_resource

class TestResourceService(unittest.TestCase):
    @patch('authentication.rbac.check_permission')
    def test_access_resource(self, mock_check_permission):
        # Test case: user with permission
        mock_check_permission.return_value = True
        result = access_resource(user_id=1, resource_id=101)
        self.assertTrue(result, "User with permission should be allowed access.")

        # Test case: user without permission
        mock_check_permission.return_value = False
        result = access_resource(user_id=2, resource_id=102)
        self.assertFalse(result, "User without permission should be denied access.")

        # Test case: invalid user ID
        mock_check_permission.side_effect = ValueError("Invalid User ID")
        with self.assertRaises(ValueError):
            access_resource(user_id='invalid', resource_id=103)

        # Test case: invalid resource ID
        mock_check_permission.side_effect = ValueError("Invalid Resource ID")
        with self.assertRaises(ValueError):
            access_resource(user_id=1, resource_id='invalid')

if __name__ == '__main__':
    unittest.main()
