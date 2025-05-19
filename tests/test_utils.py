import unittest
from unittest.mock import patch, MagicMock
from utils import send_api_request, log_test_metrics
import requests


class TestUtils(unittest.TestCase):

    @patch('utils.requests.request')
    def test_send_api_request(self, mock_request):
        # Arranging the test scenarios
        endpoint_url = "http://fakeapi.com/resource"
        request_method = "POST"
        headers = {"Content-Type": "application/json"}
        payload = {"key": "value"}

        # Mocking the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "data"}
        mock_request.return_value = mock_response

        # Executing the function to be tested
        response = send_api_request(endpoint_url, request_method, payload, headers)

        # Asserting the expected outcomes
        mock_request.assert_called_once_with(request_method, endpoint_url, headers=headers, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "data"})

    @patch('utils.requests.request')
    def test_send_api_request_error(self, mock_request):
        # Arranging the test scenarios
        endpoint_url = "http://fakeapi.com/resource"
        request_method = "POST"
        headers = {"Content-Type": "application/json"}
        payload = {"key": "value"}

        # Mocking an API error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "server_error"}
        mock_request.return_value = mock_response

        # Executing the function to be tested
        response = send_api_request(endpoint_url, request_method, payload, headers)

        # Asserting the expected outcomes
        mock_request.assert_called_once_with(request_method, endpoint_url, headers=headers, json=payload)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "server_error"})

    @patch('utils.logging.Logger.info')
    def test_log_test_metrics(self, mock_log_info):
        # Arranging the test metrics
        timestamp = "2023-10-01T12:00:00Z"
        response_time = 150
        status_code = 200
        error = None

        # Executing the function to be tested
        log_test_metrics(timestamp, response_time, status_code, error)

        # Asserting the expected outcomes
        log_message = f"Timestamp: {timestamp}, Response Time: {response_time} ms, Status Code: {status_code}, Error: {error}"
        mock_log_info.assert_called_once_with(log_message)

    @patch('utils.logging.Logger.info')
    def test_log_test_metrics_error(self, mock_log_info):
        # Arranging the test metrics with error
        timestamp = "2023-10-01T12:00:00Z"
        response_time = 2000
        status_code = 500
        error = "timeout_error"

        # Executing the function to be tested
        log_test_metrics(timestamp, response_time, status_code, error)

        # Asserting the expected outcomes
        log_message = f"Timestamp: {timestamp}, Response Time: {response_time} ms, Status Code: {status_code}, Error: {error}"
        mock_log_info.assert_called_once_with(log_message)


# This allows running the tests if this file is executed directly
if __name__ == '__main__':
    unittest.main()
