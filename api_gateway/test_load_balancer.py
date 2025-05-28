import unittest
from api_gateway.load_balancer import LoadBalancer

class TestLoadBalancer(unittest.TestCase):

    def setUp(self):
        # Sample configuration settings for initialization
        self.config = {
            'algorithm': 'round_robin', 
            'max_connections': 100
        }
        self.load_balancer = LoadBalancer(self.config)

    def test_initialize_load_balancer(self):
        """Ensure the load balancer initializes correctly with the given configuration settings."""
        self.assertEqual(self.load_balancer.algorithm, 'round_robin')
        self.assertEqual(self.load_balancer.max_connections, 100)

    def test_register_microservice(self):
        """Confirm that microservices can be registered successfully with the load balancer."""
        service = {'name': 'service1', 'url': 'http://service1-url'}
        self.load_balancer.register_microservice(service)
        self.assertIn(service, self.load_balancer.get_available_microservices())

    def test_deregister_microservice(self):
        """Ensure that microservices can be deregistered successfully and do not receive requests afterward."""
        service = {'name': 'service1', 'url': 'http://service1-url'}
        self.load_balancer.register_microservice(service)
        self.load_balancer.deregister_microservice(service['name'])
        self.assertNotIn(service, self.load_balancer.get_available_microservices())

    def test_distribute_request(self):
        """Verify that incoming requests are distributed as expected according to the load balancing algorithm."""
        service1 = {'name': 'service1', 'url': 'http://service1-url'}
        service2 = {'name': 'service2', 'url': 'http://service2-url'}
        self.load_balancer.register_microservice(service1)
        self.load_balancer.register_microservice(service2)
        
        for _ in range(10):
            chosen_service = self.load_balancer.distribute_request()
            self.assertIn(chosen_service, [service1, service2])

    def test_get_available_microservices(self):
        """Check if the list of available microservices is accurate and updated appropriately."""
        service1 = {'name': 'service1', 'url': 'http://service1-url'}
        service2 = {'name': 'service2', 'url': 'http://service2-url'}
        self.load_balancer.register_microservice(service1)
        self.load_balancer.register_microservice(service2)

        expected_services = [service1, service2]
        available_services = self.load_balancer.get_available_microservices()
        
        self.assertEqual(available_services, expected_services)

if __name__ == '__main__':
    unittest.main()
