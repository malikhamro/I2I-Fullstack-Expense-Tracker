import logging
from typing import Dict, List, Optional

class LoadBalancer:
    def __init__(self):
        self.microservices: Dict[str, Dict] = {}
        self.last_requested_service: Optional[str] = None
        logging.basicConfig(level=logging.INFO)
    
    def initialize_load_balancer(self, config: Dict[str, Any]) -> None:
        """
        Initializes the load balancer with the configuration settings for distributing requests across the available microservices.
        
        Args:
            config (Dict[str, Any]): Configuration settings for the load balancer.
        """
        logging.info("Initializing load balancer with config.")
        try:
            if not isinstance(config, dict):
                raise ValueError("Invalid configuration format. Must be a dictionary.")
            # Assuming config contains microservices and other settings
            self.microservices = config.get('microservices', {})
            logging.info("Load balancer initialized with %d microservices.", len(self.microservices))
        except Exception as e:
            logging.error("Error initializing load balancer: %s", str(e))
            raise

    def distribute_request(self, request: Dict[str, Any]) -> Dict:
        """
        Distributes an incoming request to one of the available microservices based on the load balancing algorithm.
        
        Args:
            request (Dict[str, Any]): Incoming request that needs to be processed.
        
        Returns:
            Dict: Response from the selected microservice.
        """
        logging.info("Distributing request.")
        if not self.microservices:
            raise RuntimeError("No microservices registered with the load balancer.")
        
        # Example of a simple round-robin load balancing algorithm
        microservice_keys = list(self.microservices.keys())
        if not microservice_keys:
            raise RuntimeError("No available microservices to handle the request.")
        
        if self.last_requested_service is None or self.last_requested_service == microservice_keys[-1]:
            self.last_requested_service = microservice_keys[0]
        else:
            last_index = microservice_keys.index(self.last_requested_service)
            self.last_requested_service = microservice_keys[last_index + 1]
        
        selected_service = self.microservices[self.last_requested_service]
        logging.info("Request distributed to microservice %s.", self.last_requested_service)
        # Simulate request handling by the microservice
        response = selected_service['handler_function'](request)
        
        return response
    
    def register_microservice(self, name: str, handler_function: callable, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Registers a new microservice with the load balancer to be included in the request distribution.
        
        Args:
            name (str): Name of the microservice.
            handler_function (callable): Function to handle requests for this microservice.
            metadata (Optional[Dict[str, Any]]): Additional metadata about the microservice.
        """
        logging.info("Registering microservice: %s.", name)
        if name in self.microservices:
            raise ValueError(f"Microservice {name} is already registered.")
        
        if not callable(handler_function):
            raise ValueError("Handler function must be callable.")
        
        self.microservices[name] = {
            'handler_function': handler_function,
            'metadata': metadata or {}
        }
        logging.info("Microservice %s registered successfully.", name)
    
    def deregister_microservice(self, name: str) -> None:
        """
        Deregisters a microservice from the load balancer, so it no longer receives requests.
        
        Args:
            name (str): Name of the microservice to deregister.
        """
        logging.info("Deregistering microservice: %s.", name)
        if name not in self.microservices:
            raise ValueError(f"Microservice {name} is not registered.")
        
        del self.microservices[name]
        if self.last_requested_service == name:
            self.last_requested_service = None
        
        logging.info("Microservice %s deregistered successfully.", name)
    
    def get_available_microservices(self) -> List[str]:
        """
        Returns a list of currently registered and available microservices that can handle requests.
        
        Returns:
            List[str]: List of microservice names.
        """
        logging.info("Getting available microservices.")
        return list(self.microservices.keys())

# Example usage
def example_microservice_handler(request):
    return {"status": "success", "data": request}

if __name__ == "__main__":
    lb = LoadBalancer()
    config = {
        'microservices': {
            'service1': {
                'handler_function': example_microservice_handler,
                'metadata': {}
            },
            'service2': {
                'handler_function': example_microservice_handler,
                'metadata': {}
            }
        }
    }
    lb.initialize_load_balancer(config)
    print(lb.get_available_microservices())
    response = lb.distribute_request({"request": "data"})
    print(response)
    lb.register_microservice("service3", example_microservice_handler)
    lb.deregister_microservice("service1")
    print(lb.get_available_microservices())
