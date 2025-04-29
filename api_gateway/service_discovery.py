import json
import logging
import requests
import time
from threading import Timer

# Configurations are assumed to be loaded as needed from a separate configuration module
from gateway_configuration import load_configuration

logger = logging.getLogger(__name__)
config = load_configuration()

class DiscoveryServiceError(Exception):
    pass

def connect_to_discovery_service():
    """
    Establish connection to the microservice discovery service using details from the gateway configuration.
    This function handles authentication and network communications needed to interact with the discovery service's API.
    
    Raises:
        DiscoveryServiceError: If the connection cannot be established.
    """
    discovery_service_url = config.get("discovery_service_url")
    auth_token = config.get("discovery_service_auth_token")

    if not discovery_service_url or not auth_token:
        raise DiscoveryServiceError("Discovery service URL or auth token is missing in the configuration.")

    try:
        response = requests.get(discovery_service_url, headers={"Authorization": f"Bearer {auth_token}"})
        response.raise_for_status()
        logger.info(f"Successfully connected to discovery service at {discovery_service_url}")
        return response.json()  # Return JSON response for further processing
    except requests.RequestException as e:
        logger.error(f"Failed to connect to discovery service: {e}")
        raise DiscoveryServiceError(f"Connection error: {e}")

def fetch_services():
    """
    Retrieve the list of available services from the discovery service, parsing the response to return
    a structured list of service instances.

    Returns:
        list: A structured list of service instances available for routing.
    
    Raises:
        DiscoveryServiceError: If the service fetch operation fails.
    """
    try:
        service_data = connect_to_discovery_service()
        # Example parsing logic, assuming service_data is a JSON with a key 'services'
        services = service_data.get("services", [])
        if not services:
            logger.warning("No services found in discovery service response.")
        return services
    except DiscoveryServiceError as e:
        logger.error(f"Fetching services failed: {e}")
        raise
    
def refresh_service_list(interval=60):
    """
    Periodically update the list of available services using a scheduling mechanism, invoking fetch_services
    at regular intervals.

    Args:
        interval (int): The time interval (in seconds) at which the service list should be refreshed.
    """
    def _refresh():
        try:
            services = fetch_services()
            logger.info(f"Refreshed service list: {json.dumps(services, indent=2)}")
        except DiscoveryServiceError as e:
            logger.error(f"Failed to refresh service list: {e}")
        finally:
            # Schedule the next refresh
            Timer(interval, _refresh).start()

    # Initial call to start the periodic refresh
    _refresh()
