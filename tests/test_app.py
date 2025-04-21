import unittest
from flask import Flask
from dashboard.app import create_app

class TestCreateApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_app(self):
        self.assertIsInstance(self.app, Flask, "The created app should be a Flask instance.")
        self.assertFalse(self.app.testing, "The app's testing configuration should be set to False by default.")

    def test_config(self):
        self.assertIn('DEBUG', self.app.config, "The app config should have a 'DEBUG' entry.")
        self.assertIn('SQLALCHEMY_DATABASE_URI', self.app.config, "The app config should have a 'SQLALCHEMY_DATABASE_URI' entry.")

    def test_routes_exist(self):
        # Check some common routes - these should match the actual application routes
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302], "The '/' route should return a 200 or 302 status code.")

        response = self.client.get('/migration_progress')
        self.assertIn(response.status_code, [200, 302], "The '/migration_progress' route should return a 200 or 302 status code.")

        response = self.client.get('/migration_status')
        self.assertIn(response.status_code, [200, 302], "The '/migration_status' route should return a 200 or 302 status code.")

if __name__ == '__main__':
    unittest.main()
