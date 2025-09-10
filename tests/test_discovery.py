import unittest
from unittest.mock import patch
from microservice_discovery.discovery import get_available_services

class TestMicroserviceDiscovery(unittest.TestCase):

    @patch('microservice_discovery.discovery.requests.get')
    def test_get_available_services(self, mock_get):
        # Mocked response from the microservice discovery service
        mock_response = {
            "services": [
                {"name": "service1", "endpoint": "http://service1.example.com"},
                {"name": "service2", "endpoint": "http://service2.example.com"}
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        services = get_available_services()

        self.assertEqual(len(services), 2)
        self.assertEqual(services[0]["name"], "service1")
        self.assertEqual(services[0]["endpoint"], "http://service1.example.com")
        self.assertEqual(services[1]["name"], "service2")
        self.assertEqual(services[1]["endpoint"], "http://service2.example.com")

    @patch('microservice_discovery.discovery.requests.get')
    def test_get_available_services_empty(self, mock_get):
        # Mocked response from the microservice discovery service
        mock_response = {"services": []}
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        services = get_available_services()

        self.assertEqual(len(services), 0)

    @patch('microservice_discovery.discovery.requests.get')
    def test_get_available_services_error(self, mock_get):
        # Mocked error response from the microservice discovery service
        mock_get.return_value.status_code = 500

        with self.assertRaises(Exception) as context:
            get_available_services()
        
        self.assertTrue("Error fetching services" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
