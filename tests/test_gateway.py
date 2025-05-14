import unittest
from unittest.mock import patch, MagicMock
from api_gateway.gateway import register_routes
from api_gateway.app import initialize_gateway
from microservice_discovery.discovery import get_available_services

class TestApiGateway(unittest.TestCase):

    @patch('api_gateway.gateway.get_available_services')
    @patch('api_gateway.gateway.gateway_app')
    def test_register_routes(self, mock_gateway_app, mock_get_available_services):
        # Mock the return value of get_available_services
        mock_services = [
            {'name': 'service1', 'endpoint': '/service1'},
            {'name': 'service2', 'endpoint': '/service2'}
        ]
        mock_get_available_services.return_value = mock_services

        # Call the register_routes function
        register_routes()

        # Check if routes were registered
        for service in mock_services:
            mock_gateway_app.route.assert_any_call(service['endpoint'], methods=['GET', 'POST', 'PUT', 'DELETE'])
        
        # Ensure mock_get_available_services was called once
        mock_get_available_services.assert_called_once()

    @patch('api_gateway.app.register_routes')
    @patch('api_gateway.app.gateway_app')
    def test_initialize_gateway(self, mock_gateway_app, mock_register_routes):
        # Call the initialize_gateway function
        initialize_gateway()

        # Check if middleware, routes, and configurations are set up
        mock_gateway_app.use_middleware.assert_called_once()
        
        # Ensure register_routes was called once
        mock_register_routes.assert_called_once()

if __name__ == '__main__':
    unittest.main()
