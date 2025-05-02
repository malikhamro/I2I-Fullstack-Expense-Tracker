# insurance_integration/unittests/test_providers_api.py

import unittest
from unittest.mock import patch, MagicMock
from insurance_integration import providers_api

class TestProvidersAPI(unittest.TestCase):

    @patch('insurance_integration.providers_api.requests.get')
    def test_fetch_provider_details(self, mock_get):
        # Mock response data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'provider1': {'name': 'Insurance Provider 1', 'details': 'Details about provider 1'},
            'provider2': {'name': 'Insurance Provider 2', 'details': 'Details about provider 2'}
        }
        mock_get.return_value = mock_response

        # Call the function
        provider_details = providers_api.fetch_provider_details()

        # Assertions to ensure response correctness
        self.assertIsNotNone(provider_details)
        self.assertIsInstance(provider_details, dict)
        self.assertIn('provider1', provider_details)
        self.assertIn('provider2', provider_details)
        self.assertEqual(provider_details['provider1']['name'], 'Insurance Provider 1')

        # Edge case: testing empty response
        mock_response.json.return_value = {}
        provider_details = providers_api.fetch_provider_details()
        self.assertEqual(provider_details, {})

        # Edge case: testing API failure
        mock_response.status_code = 500
        with self.assertRaises(providers_api.APIConnectionError):
            providers_api.fetch_provider_details()

if __name__ == '__main__':
    unittest.main()
