import unittest
from utils.data_analyzer import analyze_migration_data

class TestDataAnalyzer(unittest.TestCase):
        
    def setUp(self):
        """Set up test variables and data."""
        self.sample_migration_data = [
            {'task_id': 1, 'status': 'success', 'start_time': '2023-10-01T10:00:00', 'end_time': '2023-10-01T10:05:00'},
            {'task_id': 2, 'status': 'in_progress', 'start_time': '2023-10-01T10:10:00', 'end_time': None},
            {'task_id': 3, 'status': 'failed', 'start_time': '2023-10-01T10:15:00', 'end_time': '2023-10-01T10:20:00'}
        ]

    def test_analyze_migration_data_success(self):
        """Test the analysis of migration data with example data"""
        result = analyze_migration_data(self.sample_migration_data)
        
        expected_result = {
            'total_tasks': 3,
            'successful_tasks': 1,
            'tasks_in_progress': 1,
            'failed_tasks': 1,
            'average_duration': 300  # duration in seconds
        }

        self.assertEqual(result['total_tasks'], expected_result['total_tasks'])
        self.assertEqual(result['successful_tasks'], expected_result['successful_tasks'])
        self.assertEqual(result['tasks_in_progress'], expected_result['tasks_in_progress'])
        self.assertEqual(result['failed_tasks'], expected_result['failed_tasks'])
        self.assertEqual(result['average_duration'], expected_result['average_duration'])

    def test_analyze_migration_data_no_data(self):
        """Test the analysis of migration data with no data provided"""
        result = analyze_migration_data([])
        
        expected_result = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'tasks_in_progress': 0,
            'failed_tasks': 0,
            'average_duration': 0
        }

        self.assertEqual(result['total_tasks'], expected_result['total_tasks'])
        self.assertEqual(result['successful_tasks'], expected_result['successful_tasks'])
        self.assertEqual(result['tasks_in_progress'], expected_result['tasks_in_progress'])
        self.assertEqual(result['failed_tasks'], expected_result['failed_tasks'])
        self.assertEqual(result['average_duration'], expected_result['average_duration'])

    def test_analyze_migration_data_edge_cases(self):
        """Test the analysis for edge cases with varying task statuses and durations"""
        
        edge_case_data = [
            {'task_id': 4, 'status': 'success', 'start_time': '2023-10-01T11:00:00', 'end_time': '2023-10-01T20:00:00'},  # long duration
            {'task_id': 5, 'status': 'failed', 'start_time': '2023-10-01T10:25:00', 'end_time': '2023-10-01T10:25:30'},  # short duration
            {'task_id': 6, 'status': 'success', 'start_time': '2023-10-01T10:30:00', 'end_time': '2023-10-01T10:35:00'},
            {'task_id': 7, 'status': 'in_progress', 'start_time': '2023-10-01T10:45:00', 'end_time': None}  # no end time
        ]
        
        result = analyze_migration_data(edge_case_data)
        
        expected_result = {
            'total_tasks': 4,
            'successful_tasks': 2,
            'tasks_in_progress': 1,
            'failed_tasks': 1,
            'average_duration': 11580  # average duration in seconds
        }

        self.assertEqual(result['total_tasks'], expected_result['total_tasks'])
        self.assertEqual(result['successful_tasks'], expected_result['successful_tasks'])
        self.assertEqual(result['tasks_in_progress'], expected_result['tasks_in_progress'])
        self.assertEqual(result['failed_tasks'], expected_result['failed_tasks'])
        self.assertEqual(result['average_duration'], expected_result['average_duration'])

if __name__ == '__main__':
    unittest.main()
