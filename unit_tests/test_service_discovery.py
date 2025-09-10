import unittest
from unittest.mock import patch, MagicMock
from service_discovery import connect_to_discovery_service, fetch_services, refresh_service_list

class TestServiceDiscovery(unittest.TestCase):

    @patch('service_discovery.requests.post')
    def test_connect_to_discovery_service(self, mock_post):
        # Mock successful connection
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'token': 'fake_token'}
        mock_post.return_value = mock_response

        # Test success scenario
        result = connect_to_discovery_service('http://fake_discovery_service', 'fake_user', 'fake_password')
        self.assertEqual(result, 'fake_token')
        
        # Mock failed connection
        mock_response.status_code = 401
        mock_response.json.return_value = {'error': 'Unauthorized'}
        mock_post.return_value = mock_response
        
        # Test failure scenario
        with self.assertRaises(Exception) as context:
            connect_to_discovery_service('http://fake_discovery_service', 'fake_user', 'fake_password')
        self.assertTrue('Failed to connect to discovery service' in str(context.exception))

    @patch('service_discovery.requests.get')
    def test_fetch_services(self, mock_get):
        # Mock successful fetch
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'name': 'service1', 'url': 'http://service1'}, {'name': 'service2', 'url': 'http://service2'}]
        mock_get.return_value = mock_response

        # Test success scenario
        services = fetch_services('http://fake_discovery_service', 'fake_token')
        self.assertEqual(len(services), 2)
        self.assertEqual(services[0]['name'], 'service1')
        self.assertEqual(services[1]['name'], 'service2')
        
        # Mock failed fetch
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Internal Server Error'}
        mock_get.return_value = mock_response
        
        # Test failure scenario
        with self.assertRaises(Exception) as context:
            fetch_services('http://fake_discovery_service', 'fake_token')
        self.assertTrue('Failed to fetch services' in str(context.exception))

    @patch('service_discovery.fetch_services')
    @patch('service_discovery.schedule')
    def test_refresh_service_list(self, mock_schedule, mock_fetch_services):
        # Mock fetch services
        mock_fetch_services.return_value = [{'name': 'service1', 'url': 'http://service1'}]
        
        # Define a dummy callback to capture the schedule invocation
        def dummy_callback(func, *args, **kwargs):
            func()
        
        mock_schedule.every.return_value.seconds.do.side_effect = dummy_callback
        
        # Test refresh_service_list
        refresh_service_list('http://fake_discovery_service', 'fake_token', interval=1)
        
        # Assert that fetch_services was called
        mock_fetch_services.assert_called_once_with('http://fake_discovery_service', 'fake_token')
        
        # Assert that schedule has been set up correctly
        mock_schedule.every.assert_called_once_with(1)
        
if __name__ == '__main__':
    unittest.main()
