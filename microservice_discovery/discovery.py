# microservice_discovery/discovery.py

import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DISCOVERY_SERVICE_URL = "http://discovery-service.local/api/services"

def get_available_services():
    """
    Fetches the currently available services from the microservice discovery service.
    This function is called by the register_routes function in api_gateway/gateway to
    retrieve a list of available microservices and their corresponding endpoints.

    Returns:
        list: A list of dictionaries, each containing 'name' and 'endpoint' keys for a service.
    
    Raises:
        Exception: If there's an error while fetching services.
    """
    try:
        logger.info("Fetching available services from the discovery service...")
        response = requests.get(DISCOVERY_SERVICE_URL)

        # Check if request was successful
        if response.status_code != 200:
            logger.error(f"Failed to fetch services: HTTP {response.status_code}")
            response.raise_for_status()
        
        services = response.json()

        # Validate the expected structure of the response
        if not isinstance(services, list):
            raise ValueError("Unexpected response format; expected a list of services")
        
        for service in services:
            if not isinstance(service, dict) or 'name' not in service or 'endpoint' not in service:
                raise ValueError("Unexpected service format; each service must be a dictionary with 'name' and 'endpoint'")

        logger.info(f"Successfully fetched {len(services)} services.")
        return services

    except requests.RequestException as e:
        logger.exception("Exception occurred while fetching services from the discovery service.")
        raise Exception("Error while communicating with the discovery service") from e
    except ValueError as e:
        logger.error("Validation error of the services data")
        raise Exception("Service data validation error") from e

