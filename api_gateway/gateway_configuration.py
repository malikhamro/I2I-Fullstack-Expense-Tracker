import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GatewayConfigurationError(Exception):
    """Custom exception for gateway configuration errors"""
    pass

def load_configuration(config_file='gateway_config.json'):
    """
    This function will load the necessary configuration for the API Gateway to connect with the microservice discovery service.
    It will parse configuration files or environment variables to set up initial parameters for service integration.
    It provides foundational setup for other functions to utilize when establishing connections and routing logic.
    
    :param config_file: The path to the configuration file.
    :return: A dictionary with the loaded configuration.
    :raises: GatewayConfigurationError if the configuration cannot be loaded.
    """
    try:
        # Load configuration from environment variables as primary source.
        configuration = {
            'discovery_service_url': os.getenv('DISCOVERY_SERVICE_URL'),
            'api_gateway_port': os.getenv('API_GATEWAY_PORT', 8080),
            'authentication_token': os.getenv('AUTHENTICATION_TOKEN')
        }

        # Check if the configuration file exists and load it as a fallback.
        if os.path.exists(config_file):
            with open(config_file, 'r') as file:
                file_configuration = json.load(file)
                # Update the configuration with file values if they are missing
                for key, value in file_configuration.items():
                    if not configuration.get(key):
                        configuration[key] = value

        # Validate all necessary parameters are loaded
        if not all([
            configuration['discovery_service_url'],
            configuration['authentication_token']
        ]):
            missing_keys = [key for key in ['discovery_service_url', 'authentication_token'] if not configuration.get(key)]
            raise GatewayConfigurationError(f"Missing required configuration keys: {', '.join(missing_keys)}")

        logger.info("Configuration loaded successfully: %s", configuration)
        return configuration

    except (IOError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load configuration: {e}")
        raise GatewayConfigurationError("Failed to load configuration") from e


def initialize_gateway():
    """
    This function will initialize the API Gateway using the loaded configuration.
    It will set up the gateway environment, preparing it to interact with the microservice discovery service.
    This function ensures that the gateway is properly configured and authenticated before processing any service discovery or routing operations.
    
    :raises: GatewayConfigurationError if initialization fails.
    """
    try:
        # Load the configuration
        config = load_configuration()
        
        # Log the status of the initialization
        logger.info("Initializing API Gateway with configuration: %s", config)
        
        # Simulate the environment setup for the gateway
        logger.info("Setting up the API Gateway environment...")
        # In an actual implementation, this section would include authentication,
        # setting up TLS/SSL if needed, validating the discovery service connection, etc.

        logger.info("API Gateway initialized successfully with discovery service URL: %s", config['discovery_service_url'])

    except GatewayConfigurationError as e:
        logger.error(f"API Gateway initialization failed: {e}")
        raise
