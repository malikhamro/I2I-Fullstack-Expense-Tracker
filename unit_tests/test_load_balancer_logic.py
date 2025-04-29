import unittest
from unittest.mock import patch, MagicMock
from load_balancer.load_balancer_logic import distribute_requests_to_services, health_check_services

class TestLoadBalancerLogic(unittest.TestCase):
    @patch('load_balancer.load_balancer_logic.fetch_services')
    def test_distribute_requests_to_services(self, mock_fetch_services):
        # Mock the response from fetch_services
        services = [
            {'id': 'service1', 'address': 'http://localhost:5001'},
            {'id': 'service2', 'address': 'http://localhost:5002'},
            {'id': 'service3', 'address': 'http://localhost:5003'}
        ]
        mock_fetch_services.return_value = services

        request = MagicMock()
        strategy = 'round_robin'

        response1 = distribute_requests_to_services(request, strategy)
        response2 = distribute_requests_to_services(request, strategy)
        response3 = distribute_requests_to_services(request, strategy)

        self.assertEqual(response1, services[0])
        self.assertEqual(response2, services[1])
        self.assertEqual(response3, services[2])

    @patch('load_balancer.load_balancer_logic.fetch_services')
    def test_distribute_requests_to_services_empty_services(self, mock_fetch_services):
        # Mock the response from fetch_services as empty list
        mock_fetch_services.return_value = []

        request = MagicMock()
        strategy = 'round_robin'

        with self.assertRaises(Exception) as context:
            distribute_requests_to_services(request, strategy)
        
        self.assertTrue('No services available' in str(context.exception))

    @patch('load_balancer.load_balancer_logic.fetch_services')
    @patch('load_balancer.load_balancer_logic.perform_health_check')
    def test_health_check_services(self, mock_perform_health_check, mock_fetch_services):
        # Mock the response from fetch_services
        services = [
            {'id': 'service1', 'address': 'http://localhost:5001'},
            {'id': 'service2', 'address': 'http://localhost:5002', 'health': 'unhealthy'},
            {'id': 'service3', 'address': 'http://localhost:5003'}
        ]
        mock_fetch_services.return_value = services
        
        # Mock the health check results
        mock_perform_health_check.side_effect = lambda service: service.get('health', 'healthy') == 'healthy'

        healthy_services = health_check_services()

        expected_healthy_services = [
            {'id': 'service1', 'address': 'http://localhost:5001'},
            {'id': 'service3', 'address': 'http://localhost:5003'}
        ]

        self.assertEqual(healthy_services, expected_healthy_services)

    @patch('load_balancer.load_balancer_logic.fetch_services')
    @patch('load_balancer.load_balancer_logic.perform_health_check')
    def test_health_check_services_all_unhealthy(self, mock_perform_health_check, mock_fetch_services):
        # Mock the response from fetch_services
        services = [
            {'id': 'service1', 'address': 'http://localhost:5001', 'health': 'unhealthy'},
            {'id': 'service2', 'address': 'http://localhost:5002', 'health': 'unhealthy'}
        ]
        mock_fetch_services.return_value = services
        
        # Mock the health check results
        mock_perform_health_check.side_effect = lambda service: service.get('health', 'healthy') == 'healthy'

        healthy_services = health_check_services()

        expected_healthy_services = []

        self.assertEqual(healthy_services, expected_healthy_services)


if __name__ == '__main__':
    unittest.main()
