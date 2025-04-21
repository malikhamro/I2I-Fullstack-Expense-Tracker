import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from config_ui.app import create_app_instance
from config_ui.controllers.route_controller import get_routes, add_route, update_route, delete_route

class TestRouteController(unittest.TestCase):

    def setUp(self):
        self.app = create_app_instance()
        self.client = self.app.test_client()

    @patch('config_ui.controllers.route_controller.get_routes')
    def test_get_routes(self, mock_get_routes):
        mock_get_routes.return_value = [{'id': 1, 'name': 'route1', 'path': '/route1'}]
        response = self.client.get('/routes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'id': 1, 'name': 'route1', 'path': '/route1'}])
    
    @patch('config_ui.controllers.route_controller.add_route')
    def test_add_route(self, mock_add_route):
        mock_add_route.return_value = {'id': 2, 'name': 'route2', 'path': '/route2'}
        route_data = {'name': 'route2', 'path': '/route2'}
        response = self.client.post('/routes', json=route_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'id': 2, 'name': 'route2', 'path': '/route2'})
    
    @patch('config_ui.controllers.route_controller.update_route')
    def test_update_route(self, mock_update_route):
        mock_update_route.return_value = {'id': 2, 'name': 'route2_updated', 'path': '/route2'}
        route_data = {'name': 'route2_updated'}
        response = self.client.put('/routes/2', json=route_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 2, 'name': 'route2_updated', 'path': '/route2'})
    
    @patch('config_ui.controllers.route_controller.delete_route')
    def test_delete_route(self, mock_delete_route):
        mock_delete_route.return_value = {'message': 'Route deleted successfully'}
        response = self.client.delete('/routes/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Route deleted successfully'})

if __name__ == '__main__':
    unittest.main()
