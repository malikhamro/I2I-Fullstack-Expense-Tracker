import json
import unittest
from flask import Flask, jsonify, request
from flask.testing import FlaskClient

# Mocking the main Flask app for testing
app = Flask(__name__)

# Assuming the controller functions are defined somewhere
from controllers.permissions_controller import (
    create_permission,
    delete_permission,
    assign_permission_to_role,
    revoke_permission_from_role,
    get_permissions,
    get_role_permissions,
    update_permission_details,
)

# Registering routes for testing
@app.route('/permissions', methods=['POST'])
def create_permission_route():
    return create_permission()

@app.route('/permissions/<int:permission_id>', methods=['DELETE'])
def delete_permission_route(permission_id):
    return delete_permission(permission_id)

@app.route('/roles/<int:role_id>/permissions/<int:permission_id>', methods=['POST'])
def assign_permission_to_role_route(role_id, permission_id):
    return assign_permission_to_role(role_id, permission_id)

@app.route('/roles/<int:role_id>/permissions/<int:permission_id>', methods=['DELETE'])
def revoke_permission_from_role_route(role_id, permission_id):
    return revoke_permission_from_role(role_id, permission_id)

@app.route('/permissions', methods=['GET'])
def get_permissions_route():
    return get_permissions()

@app.route('/roles/<int:role_id>/permissions', methods=['GET'])
def get_role_permissions_route(role_id):
    return get_role_permissions(role_id)

@app.route('/permissions/<int:permission_id>', methods=['PUT'])
def update_permission_details_route(permission_id):
    return update_permission_details(permission_id)

class PermissionsControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_permission_api(self):
        response = self.app.post('/permissions', json={
            'name': 'test_permission',
            'description': 'A test permission'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('permission_id', json.loads(response.data))

    def test_delete_permission_api(self):
        permission_id = 1  # Example ID for testing
        response = self.app.delete(f'/permissions/{permission_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.data))

    def test_assign_permission_to_role_api(self):
        role_id = 1  # Example ID for testing
        permission_id = 1  # Example ID for testing
        response = self.app.post(f'/roles/{role_id}/permissions/{permission_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.data))

    def test_revoke_permission_from_role_api(self):
        role_id = 1  # Example ID for testing
        permission_id = 1  # Example ID for testing
        response = self.app.delete(f'/roles/{role_id}/permissions/{permission_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.data))

    def test_get_permissions_api(self):
        response = self.app.get('/permissions')
        self.assertEqual(response.status_code, 200)
        self.assertIn('permissions', json.loads(response.data))

    def test_get_role_permissions_api(self):
        role_id = 1  # Example ID for testing
        response = self.app.get(f'/roles/{role_id}/permissions')
        self.assertEqual(response.status_code, 200)
        self.assertIn('permissions', json.loads(response.data))

    def test_update_permission_details_api(self):
        permission_id = 1  # Example ID for testing
        response = self.app.put(f'/permissions/{permission_id}', json={
            'name': 'updated_permission',
            'description': 'An updated test permission'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.data))

if __name__ == '__main__':
    unittest.main()
