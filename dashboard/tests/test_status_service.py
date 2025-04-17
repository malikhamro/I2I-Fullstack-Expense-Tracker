# dashboard/tests/test_status_service.py

import unittest
from dashboard.services.status_service import check_migration_status

class TestStatusService(unittest.TestCase):
    
    def test_check_migration_status(self):
        """
        Unit test for check_migration_status function to ensure it checks status correctly.
        This test case will cover various scenarios including normal operation and edge cases.
        """
        # Define mock data for various scenarios
        mock_status_data_normal = {
            "status": "success",
            "details": {
                "total_migrations": 120,
                "successful_migrations": 118,
                "pending_migrations": 2
            }
        }
        
        mock_status_data_failure = {
            "status": "failure",
            "error": "Database connection lost",
            "details": {
                "total_migrations": 120,
                "successful_migrations": 100,
                "pending_migrations": 20
            }
        }

        mock_status_data_edge = {
            "status": "success",
            "details": {
                "total_migrations": 1,
                "successful_migrations": 0,
                "pending_migrations": 1
            }
        }

        # Mock the data retrieval inside check_migration_status function
        def mock_fetch_status_data():
            # This is where we'd integrate with a real data source, but we'll simulate it here
            data_source = {
                'normal': mock_status_data_normal,
                'failure': mock_status_data_failure,
                'edge': mock_status_data_edge
            }
            return data_source.get('normal')  # Change 'normal' to 'failure', 'edge' to test other scenarios

        # Patch the actual data fetching method
        original_fetch_status_data = check_migration_status.__globals__['fetch_status_data']
        check_migration_status.__globals__['fetch_status_data'] = mock_fetch_status_data

        try:
            # Normal scenario test
            result = check_migration_status()
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['details']['total_migrations'], 120)
            self.assertEqual(result['details']['successful_migrations'], 118)
            self.assertEqual(result['details']['pending_migrations'], 2)

            # Testing failure scenario
            check_migration_status.__globals__['fetch_status_data'] = lambda: mock_status_data_failure
            result = check_migration_status()
            self.assertEqual(result['status'], 'failure')
            self.assertIn('error', result)
            self.assertEqual(result['details']['total_migrations'], 120)
            self.assertEqual(result['details']['successful_migrations'], 100)

            # Testing edge case scenario
            check_migration_status.__globals__['fetch_status_data'] = lambda: mock_status_data_edge
            result = check_migration_status()
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['details']['total_migrations'], 1)
            self.assertEqual(result['details']['pending_migrations'], 1)

        finally:
            # Restore the original method
            check_migration_status.__globals__['fetch_status_data'] = original_fetch_status_data

if __name__ == '__main__':
    unittest.main()
