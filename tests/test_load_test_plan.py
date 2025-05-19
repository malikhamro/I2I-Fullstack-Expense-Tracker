# tests/test_load_test_plan.py

import unittest
from unittest.mock import patch
from api_load_testing.load_test_plan import (
    create_load_test_scenarios,
    generate_test_data,
    execute_load_tests,
    analyze_test_results
)
from utils import send_api_request, log_test_metrics

class TestLoadTestPlan(unittest.TestCase):
    
    def test_create_load_test_scenarios(self):
        scenarios = create_load_test_scenarios()
        self.assertIsInstance(scenarios, list, "Scenarios should be a list of test definitions.")
        self.assertGreater(len(scenarios), 0, "Scenarios list should not be empty.")

        for scenario in scenarios:
            self.assertIn('criteria', scenario, "Scenario should include 'criteria'.")
            self.assertIn('parameters', scenario, "Scenario should include 'parameters'.")
            self.assertIn('expected_outcome', scenario, "Scenario should include 'expected_outcome'.")

    def test_generate_test_data(self):
        test_data = generate_test_data()
        self.assertNotEqual(len(test_data), 0, "Test data should not be empty.")
        
        for data_set in test_data:
            self.assertIn('user_role', data_set, "Data set should include 'user_role'.")
            self.assertIn('request_type', data_set, "Data set should include 'request_type'.")

    @patch('api_load_testing.load_test_plan.send_api_request')
    def test_execute_load_tests(self, mock_send_api_request):
        mock_send_api_request.return_value = {'status_code': 200, 'response_time': 150}
        scenarios = create_load_test_scenarios()
        
        metrics = execute_load_tests(scenarios)
        self.assertIsNotNone(metrics, "Metrics should be collected during test execution.")

        for metric in metrics:
            self.assertIn('response_time', metric, "Metric should include 'response_time'.")
            self.assertIn('status_code', metric, "Metric should include 'status_code'.")

        mock_send_api_request.assert_called()

    def test_analyze_test_results(self):
        test_metrics = [
            {'response_time': 150, 'status_code': 200},
            {'response_time': 250, 'status_code': 500},
        ]

        results = analyze_test_results(test_metrics)

        self.assertIsInstance(results, dict, "Results should be returned as a dictionary.")
        self.assertIn('bottlenecks', results, "Results should include information about 'bottlenecks'.")
        self.assertIn('performance_insights', results, "Results should include 'performance_insights'.")

if __name__ == '__main__':
    unittest.main()
