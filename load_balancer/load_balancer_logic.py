# load_balancer/load_balancer_logic.py

import random
from datetime import datetime, timedelta
import requests
from service_discovery import fetch_services

# Configuration for health check intervals
HEALTH_CHECK_INTERVAL = timedelta(seconds=30)
LAST_HEALTH_CHECK = datetime.min

# Placeholder for available services
AVAILABLE_SERVICES = []

def distribute_requests_to_services(request_data):
    """
    This function will use the list of available services from service_discovery.py:fetch_services 
    to route incoming requests. It applies specific load balancing algorithms (e.g., round-robin, 
    least connections) to distribute traffic evenly across services, optimizing performance and 
    resource utilization.
    
    :param request_data: The request data that needs to be routed
    :return: Response from the chosen service
    """
    global AVAILABLE_SERVICES
    
    if not AVAILABLE_SERVICES:
        AVAILABLE_SERVICES = fetch_services()

    if not AVAILABLE_SERVICES:
        raise Exception("No available services to route the request to")

    # Implementing round-robin load balancing
    service_instance = AVAILABLE_SERVICES.pop(0)
    AVAILABLE_SERVICES.append(service_instance)
    
    try:
        response = requests.post(service_instance['url'], json=request_data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Error forwarding the request to {service_instance['url']}: {str(e)}")


def perform_health_check():
    """
    This function checks the health of services obtained via service_discovery.py:fetch_services
    and ensures that only healthy services are in the rotation for request handling.
    """
    global AVAILABLE_SERVICES

    healthy_services = []

    for service in AVAILABLE_SERVICES:
        try:
            health_response = requests.get(f"{service['url']}/health")
            health_response.raise_for_status()

            health_data = health_response.json()
            if health_data.get("status") == "healthy":
                healthy_services.append(service)
        except requests.RequestException:
            continue  # Skip unhealthy or unreachable services
    
    return healthy_services

def health_check_services():
    """
    This function regularly checks the health of services obtained via service_discovery.py:fetch_services.
    """
    global LAST_HEALTH_CHECK
    global AVAILABLE_SERVICES

    now = datetime.now()
    if now - LAST_HEALTH_CHECK >= HEALTH_CHECK_INTERVAL:
        LAST_HEALTH_CHECK = now
        AVAILABLE_SERVICES = perform_health_check()


# Schedule health check service to run periodically
import threading

def schedule_health_checks():
    """
    Schedule the health check to run at regular intervals
    """
    health_check_services()
    threading.Timer(HEALTH_CHECK_INTERVAL.total_seconds(), schedule_health_checks).start()

# Start the scheduled health checks
schedule_health_checks()
