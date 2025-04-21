import unittest
from unittest.mock import patch
from dashboard.controllers.dashboard_controller import update_dashboard_view, get_migration_summary

class TestDashboardController(unittest.TestCase):
    
    @patch('dashboard.controllers.dashboard_controller.fetch_migration_data')
    @patch('dashboard.controllers.dashboard_controller.aggregate_migration_data')
    def test_update_dashboard_view(self, mock_aggregate_migration_data, mock_fetch_migration_data):
        # Mock data setup
        raw_data = [{'id': 1, 'status': 'completed'}, {'id': 2, 'status': 'in progress'}]
        aggregated_data = {'completed': 1, 'in_progress': 1}
        
        mock_fetch_migration_data.return_value = raw_data
        mock_aggregate_migration_data.return_value = aggregated_data
        
        # Calling the function
        result = update_dashboard_view()
        
        # Assertions
        mock_fetch_migration_data.assert_called_once()
        mock_aggregate_migration_data.assert_called_once_with(raw_data)
        self.assertEqual(result, aggregated_data)

    @patch('dashboard.controllers.dashboard_controller.fetch_migration_data')
    def test_get_migration_summary(self, mock_fetch_migration_data):
        # Mock data setup
        raw_data = [{'id': 1, 'status': 'completed'}, {'id': 2, 'status': 'in progress'}]
        migration_summary = "Completed: 1, In Progress: 1"
        
        mock_fetch_migration_data.return_value = raw_data
        
        # Calling the function
        result = get_migration_summary()
        
        # Assertions
        mock_fetch_migration_data.assert_called_once()
        self.assertEqual(result, migration_summary)

if __name__ == '__main__':
    unittest.main()
