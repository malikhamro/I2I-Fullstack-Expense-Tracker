import unittest
from unittest.mock import patch, MagicMock
from config_ui.app import create_app_instance
from config_ui.controllers.policy_controller import get_policies, add_policy, update_policy, delete_policy

class TestPolicyEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app_instance()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('config_ui.controllers.policy_controller.get_policies')
    def test_get_policies(self, mock_get_policies):
        # Setup mock
        mock_get_policies.return_value = ([
            {'id': 1, 'name': 'Policy One', 'rules': []},
            {'id': 2, 'name': 'Policy Two', 'rules': []}
        ], 200)
        
        # Perform test
        response = self.client.get('/api/policies')
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        mock_get_policies.assert_called_once()

    @patch('config_ui.controllers.policy_controller.add_policy')
    def test_add_policy(self, mock_add_policy):
        # Setup mock
        policy_to_add = {'id': 3, 'name': 'Policy Three', 'rules': []}
        mock_add_policy.return_value = (policy_to_add, 201)

        # Perform test
        response = self.client.post('/api/policies', json=policy_to_add)
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['id'], policy_to_add['id'])
        self.assertEqual(data['name'], policy_to_add['name'])
        mock_add_policy.assert_called_once_with()

    @patch('config_ui.controllers.policy_controller.update_policy')
    def test_update_policy(self, mock_update_policy):
        # Setup mock
        policy_id = 1
        updated_policy = {'id': policy_id, 'name': 'Updated Policy One', 'rules': []}
        mock_update_policy.return_value = (updated_policy, 200)

        # Perform test
        response = self.client.put(f'/api/policies/{policy_id}', json=updated_policy)
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], policy_id)
        self.assertEqual(data['name'], 'Updated Policy One')
        mock_update_policy.assert_called_once_with(policy_id, updated_policy)

    @patch('config_ui.controllers.policy_controller.delete_policy')
    def test_delete_policy(self, mock_delete_policy):
        # Setup mock
        policy_id = 2
        mock_delete_policy.return_value = ({'message': 'Policy deleted successfully'}, 200)

        # Perform test
        response = self.client.delete(f'/api/policies/{policy_id}')
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Policy deleted successfully')
        mock_delete_policy.assert_called_once_with(policy_id)

if __name__ == '__main__':
    unittest.main()
