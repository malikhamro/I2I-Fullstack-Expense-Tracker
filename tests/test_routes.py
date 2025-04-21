# tests/test_routes.py

import unittest
from flask import Flask, json
from dashboard.app import create_app
from dashboard.routes import init_routes

class TestRoutes(unittest.TestCase):
    def setUp(self):
        """Set up a test client for the Flask application."""
        self.app = create_app()
        # We need testing flag and context management to test Flask application.
        self.app.testing = True
        self.client = self.app.test_client()
        with self.app.app_context():
            init_routes()

    def test_migration_progress_route(self):
        """Test if the migration progress route returns the correct response."""
        response = self.client.get('/migration-progress')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('progress', data)  # Verify that 'progress' is in the response data

    def test_migration_status_route(self):
        """Test if the migration status route returns the correct response."""
        response = self.client.get('/migration-status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)  # Verify that 'status' is in the response data

if __name__ == '__main__':
    unittest.main()
