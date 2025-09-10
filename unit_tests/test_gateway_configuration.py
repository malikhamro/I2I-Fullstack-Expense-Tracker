import unittest
from unittest.mock import patch, mock_open
import os
import json
from api_gateway.gateway_configuration import load_configuration, initialize_gateway

class TestGatewayConfiguration(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"service_url": "http://localhost:8080", "auth_token": "1234567890"}')
    def test_load_configuration_from_file(self, mock_file):
        # Assuming load_configuration uses configuration.json
        config = load_configuration("configuration.json")
        self.assertEqual(config['service_url'], "http://localhost:8080")
        self.assertEqual(config['auth_token'], "1234567890")

    @patch('os.getenv')
    def test_load_configuration_from_env(self, mock_getenv):
        # Setting up mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            "SERVICE_URL": "http://localhost:8080",
            "AUTH_TOKEN": "1234567890"
        }.get(key, default)

        config = load_configuration()
        self.assertEqual(config['service_url'], "http://localhost:8080")
        self.assertEqual(config['auth_token'], "1234567890")

    @patch('builtins.open', new_callable=mock_open, read_data='{"invalid_json": ')
    def test_load_configuration_with_invalid_file(self, mock_file):
        with self.assertRaises(json.JSONDecodeError):
            load_configuration("invalid_config.json")

    @patch('os.getenv')
    def test_load_configuration_with_missing_env_vars(self, mock_getenv):
        mock_getenv.side_effect = lambda key, default=None: {
            "SERVICE_URL": None,
            "AUTH_TOKEN": None
        }.get(key, default)

        with self.assertRaises(ValueError):
            load_configuration()

    @patch('api_gateway.gateway_configuration.load_configuration')
    def test_initialize_gateway(self, mock_load_configuration):
        mock_load_configuration.return_value = {
            "service_url": "http://localhost:8080",
            "auth_token": "1234567890"
        }

        result = initialize_gateway()
        self.assertTrue(result)
        self.assertEqual(result['environment'], 'initialized')
        self.assertEqual(result['auth_status'], 'authenticated')

if __name__ == '__main__':
    unittest.main()
