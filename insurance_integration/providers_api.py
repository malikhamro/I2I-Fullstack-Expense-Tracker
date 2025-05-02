import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

PROVIDER_ENDPOINTS = {
    'ProviderA': 'https://api.providera.com/details',
    'ProviderB': 'https://api.providerb.com/details',
    # Add additional providers here
}

def fetch_provider_details():
    """
    Fetch details from various insurance providers' APIs.
    
    This function attempts to make API calls to fetch provider details from multiple
    endpoints. It handles the responses accordingly and logs any issues encountered.

    Returns:
        dict: A dictionary with provider names as keys and their details or error messages as values.
    """
    provider_details = {}

    for provider, endpoint in PROVIDER_ENDPOINTS.items():
        try:
            response = requests.get(endpoint, timeout=10)  # Adjust timeout value as needed
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

            provider_details[provider] = response.json()  # Assuming the API returns JSON response
        except (HTTPError, ConnectionError, Timeout) as http_err:
            provider_details[provider] = f'HTTP error occurred: {http_err}'
        except RequestException as req_err:
            provider_details[provider] = f'Request error occurred: {req_err}'
        except Exception as err:
            provider_details[provider] = f'An unexpected error occurred: {err}'

    return provider_details

if __name__ == '__main__':
    results = fetch_provider_details()
    for provider, details in results.items():
        print(f'{provider}: {details}')
