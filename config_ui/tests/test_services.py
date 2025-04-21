import unittest
from unittest.mock import patch, MagicMock
from config_ui.app import create_app_instance

class TestServiceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app_instance()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('config_ui.controllers.service_controller.get_services')
    def test_get_services(self, mock_get_services):
        mock_services = [
            {'id': 1, 'name': 'Service1'},
            {'id': 2, 'name': 'Service2'}
        ]
        mock_get_services.return_value = mock_services

        response = self.client.get('/services')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_services)

    @patch('config_ui.controllers.service_controller.add_service')
    def test_add_service(self, mock_add_service):
        new_service = {'name': 'NewService'}
        mock_add_service.return_value = {'id': 3, 'name': 'NewService'}

        response = self.client.post('/services', json=new_service)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'id': 3, 'name': 'NewService'})

    @patch('config_ui.controllers.service_controller.update_service')
    def test_update_service(self, mock_update_service):
        updated_service = {'id': 1, 'name': 'UpdatedService'}
        mock_update_service.return_value = updated_service

        response = self.client.put('/services/1', json=updated_service)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, updated_service)

    @patch('config_ui.controllers.service_controller.delete_service')
    def test_delete_service(self, mock_delete_service):
        mock_delete_service.return_value = {'message': 'Service deleted'}

        response = self.client.delete('/services/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Service deleted'})

if __name__ == '__main__':
    unittest.main()
