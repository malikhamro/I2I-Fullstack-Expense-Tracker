import unittest
from unittest.mock import patch
from data_consistency.policy_storage import store_policy, retrieve_policy, update_policy

class TestPolicyStorage(unittest.TestCase):
    
    @patch('data_consistency.policy_storage.store_policy')
    def test_store_policy(self, mock_store_policy):
        # Define a sample policy to store
        sample_policy = {
            "policy_name": "Test Policy",
            "rules": [
                {"rule": "Rule 1", "condition": "Condition 1"},
                {"rule": "Rule 2", "condition": "Condition 2"}
            ]
        }
        
        # Simulate storing the policy without any side effects
        mock_store_policy.return_value = True
        
        # Call the function with the sample policy
        result = store_policy(sample_policy)
        
        # Assert that the function was called with the correct parameters
        mock_store_policy.assert_called_with(sample_policy)
        
        # Assert the function returned True indicating successful storage
        self.assertTrue(result)

    @patch('data_consistency.policy_storage.retrieve_policy')
    def test_retrieve_policy(self, mock_retrieve_policy):
        # Define a sample policy name to retrieve
        policy_name = "Test Policy"
        
        # Define what the mock should return when called
        stored_policy = {
            "policy_name": "Test Policy",
            "rules": [
                {"rule": "Rule 1", "condition": "Condition 1"},
                {"rule": "Rule 2", "condition": "Condition 2"}
            ]
        }
        mock_retrieve_policy.return_value = stored_policy
        
        # Call the function with the policy name
        result = retrieve_policy(policy_name)
        
        # Assert that the function was called with the correct parameters
        mock_retrieve_policy.assert_called_with(policy_name)
        
        # Assert the function returned the stored policy correctly
        self.assertEqual(result, stored_policy)

    @patch('data_consistency.policy_storage.update_policy')
    def test_update_policy(self, mock_update_policy):
        # Define a sample policy to update
        sample_policy = {
            "policy_name": "Test Policy",
            "rules": [
                {"rule": "Updated Rule 1", "condition": "Updated Condition 1"},
                {"rule": "Updated Rule 2", "condition": "Updated Condition 2"}
            ]
        }
        
        # Simulate updating the policy without any side effects
        mock_update_policy.return_value = True
        
        # Call the function with the sample policy
        result = update_policy(sample_policy)
        
        # Assert that the function was called with the correct parameters
        mock_update_policy.assert_called_with(sample_policy)
        
        # Assert the function returned True indicating successful update
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
