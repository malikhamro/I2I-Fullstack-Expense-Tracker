import logging
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Dummy implementation of microservice_discovery's get_available_services
def get_available_services():
    # This function should interact with the microservice discovery service
    # and return a list of available services and their endpoints.
    # Example response format:
    # [{'name': 'service1', 'url': '/service1'}, {'name': 'service2', 'url': '/service2'}]
    
    # For demonstration, return a static list
    return [
        {'name': 'service1', 'url': '/service1', 'methods': ['GET']},
        {'name': 'service2', 'url': '/service2', 'methods': ['POST']}
    ]

def register_routes(app):
    """
    Registers various service routes dynamically using the microservice discovery service.
    This function retrieves available services from microservice_discovery:get_available_services
    and sets up routes in the API Gateway.
    
    :param app: Flask application instance
    """
    try:
        services = get_available_services()
        if not services:
            logger.error("No services available to register.")
            raise RuntimeError("No services available")
        
        for service in services:
            name = service.get('name')
            url = service.get('url')
            methods = service.get('methods', ['GET'])

            if not name or not url or not isinstance(methods, list):
                logger.error(f"Invalid service definition: {service}")
                raise ValueError(f"Invalid service definition: {service}")

            # Register route with Flask application
            @app.route(url, methods=methods)
            def handle_request():
                response = {"message": f"Handling request for {name} at {url}"}
                return jsonify(response)
            
            logger.info(f"Registered {name} at {url} with methods {methods}")

    except HTTPException as http_err:
        logger.error(f"HTTP Error occurred: {http_err}")
        raise

    except Exception as err:
        logger.error(f"An error occurred during route registration: {err}")
        raise

# Sample usage:
if __name__ == '__main__':
    app = Flask(__name__)
    register_routes(app)
    
    app.run(debug=True)
