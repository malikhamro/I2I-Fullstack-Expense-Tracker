import unittest
from unittest.mock import patch, MagicMock
from data_consistency.consistency_checker import ConsistencyChecker

class TestConsistencyChecker(unittest.TestCase):

    @patch('data_consistency.consistency_checker.DatabaseClient')
    def test_check_consistency(self, MockDatabaseClient):
        """
        Unit test for checking data consistency.
        """
        mock_db_client = MockDatabaseClient.return_value
        mock_db_client.get_data.return_value = {
            'service_a': {'id': 1, 'value': 'data_a'},
            'service_b': {'id': 1, 'value': 'data_a'}
        }
        
        checker = ConsistencyChecker(mock_db_client)
        result = checker.check_consistency()
        
        self.assertTrue(result)

    @patch('data_consistency.consistency_checker.Logger')
    @patch('data_consistency.consistency_checker.DatabaseClient')
    def test_log_inconsistencies(self, MockDatabaseClient, MockLogger):
        """
        Unit test for logging inconsistencies.
        """
        mock_db_client = MockDatabaseClient.return_value
        mock_logger = MockLogger.return_value
        mock_db_client.get_data.return_value = {
            'service_a': {'id': 1, 'value': 'data_a'},
            'service_b': {'id': 1, 'value': 'data_b'}
        }

        checker = ConsistencyChecker(mock_db_client)
        checker.log_inconsistencies()
        
        mock_logger.log.assert_called_once_with("Inconsistency found: service_a vs service_b")
        
    @patch('data_consistency.consistency_checker.ReportGenerator')
    @patch('data_consistency.consistency_checker.DatabaseClient')
    def test_generate_consistency_report(self, MockDatabaseClient, MockReportGenerator):
        """
        Unit test for generating consistency reports.
        """
        mock_db_client = MockDatabaseClient.return_value
        mock_report_generator = MockReportGenerator.return_value
        mock_db_client.get_data.return_value = {
            'service_a': {'id': 1, 'value': 'data_a'},
            'service_b': {'id': 1, 'value': 'data_a'}
        }

        checker = ConsistencyChecker(mock_db_client)
        report = checker.generate_consistency_report()
        
        mock_report_generator.generate.assert_called_once_with({
            'service_a': {'id': 1, 'value': 'data_a'},
            'service_b': {'id': 1, 'value': 'data_a'}
        })
        self.assertEqual(report, "Consistency Report: All data is consistent.")

if __name__ == '__main__':
    unittest.main()
