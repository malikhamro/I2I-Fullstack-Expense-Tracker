# config_ui/services/service_service.py

from typing import List, Dict, Any
from models.service_model import Service, from_dict, to_dict

def list_services() -> List[Dict[str, Any]]:
    """ Business logic for listing services. """
    try:
        # Here would be the logic to fetch services from the data source, e.g., a database.
        services = fetch_services_from_db()  # This is a placeholder function
        return [to_dict(service) for service in services]
    except Exception as e:
        # Adding error handling for database fetching issues
        print(f"Error fetching services: {e}")
        return []

def create_service(service_data: Dict[str, Any]) -> Dict[str, Any]:
    """ Business logic for creating a new service. """
    try:
        # Convert input dictionary to a Service object
        service = from_dict(service_data)
        
        # Here would be the logic to save the service to the data source
        saved_service = save_service_to_db(service)  # This is a placeholder function
        return to_dict(saved_service)
    except ValueError as ve:
        # Handle value errors that might come from from_dict conversions
        print(f"Error converting service data: {ve}")
        return {}
    except Exception as e:
        # General exception handling for any unexpected issues
        print(f"Error creating service: {e}")
        return {}

def edit_service(service_id: int, updated_data: Dict[str, Any]) -> Dict[str, Any]:
    """ Business logic for editing an existing service. """
    try:
        # Fetch the existing service to be updated
        existing_service = fetch_service_by_id_from_db(service_id)  # This is a placeholder function
        
        # Update the service with new data
        for key, value in updated_data.items():
            setattr(existing_service, key, value)
        
        # Save the updated service back to the data source
        updated_service = save_service_to_db(existing_service)  # This is a placeholder function
        return to_dict(updated_service)
    except KeyError as ke:
        # Handle cases where the service_id doesn't exist
        print(f"Service ID not found: {ke}")
        return {}
    except Exception as e:
        # General exception handling for any unexpected issues
        print(f"Error updating service: {e}")
        return {}

def remove_service(service_id: int) -> bool:
    """ Business logic for removing a service. """
    try:
        # Logic to remove the service from the data source.
        result = delete_service_from_db(service_id)  # This is a placeholder function
        return result
    except KeyError as ke:
        # Handle cases where the service_id doesn't exist
        print(f"Service ID not found: {ke}")
        return False
    except Exception as e:
        # General exception handling for any unexpected issues
        print(f"Error deleting service: {e}")
        return False

# Note: The placeholder functions like fetch_services_from_db, save_service_to_db, 
# fetch_service_by_id_from_db and delete_service_from_db need to be implemented to interact 
# with the actual data source (could be a database or other storage mechanism).
