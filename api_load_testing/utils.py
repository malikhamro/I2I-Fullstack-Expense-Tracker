import requests
import logging
import datetime

# Set up logging configuration
logging.basicConfig(filename='api_load_testing.log', level=logging.INFO, format='%(asctime)s %(message)s')

def send_api_request(url, method='GET', headers=None, payload=None):
    """
    This function will handle the actual sending of API requests as part of the load testing process.
    It will incorporate details such as endpoint URLs, request methods, headers, and payload data generated from generate_test_data.
    The function will log request and response details for further analysis.
    
    Params:
    - url (str): The endpoint URL for the API request.
    - method (str): The HTTP method to be used for the API request (e.g., 'GET', 'POST', etc.). Default is 'GET'.
    - headers (dict): Headers to be included in the API request. Default is None.
    - payload (dict): Payload data to be sent with the API request. Default is None.
    """
    try:
        response = requests.request(method, url, headers=headers, json=payload)
        log_test_metrics(url, method, headers, payload, response)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during API request: {e}")
        log_test_metrics(url, method, headers, payload, None, error=str(e))
        return None

def log_test_metrics(url, method, headers, payload, response, error=None):
    """
    This function will systematically record the metrics obtained during the load tests execution.
    It will log details such as timestamp, response time, status codes, and any errors encountered.
    These logs will be used by analyze_test_results for thorough evaluation of API performance.
    
    Params:
    - url (str): The endpoint URL for the API request.
    - method (str): The HTTP method used for the API request.
    - headers (dict): Headers included in the API request.
    - payload (dict): Payload data sent with the API request.
    - response (requests.Response): Response object returned from the API request.
    - error (str): Any error encountered during the API request. Default is None.
    """
    timestamp = datetime.datetime.now().isoformat()
    response_time = response.elapsed.total_seconds() if response else None
    status_code = response.status_code if response else 'N/A'
    response_content = response.content if response else 'N/A'
    
    logging.info({
        'timestamp': timestamp,
        'url': url,
        'method': method,
        'headers': headers,
        'payload': payload,
        'status_code': status_code,
        'response_time': response_time,
        'response_content': response_content,
        'error': error
    })
