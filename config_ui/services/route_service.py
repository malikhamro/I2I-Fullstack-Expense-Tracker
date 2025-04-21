# config_ui/services/route_service.py

from typing import List, Dict, Any, Optional
from config_ui.models.route_model import Route

def list_routes() -> List[Dict[str, Any]]:
    """
    Business logic for listing routes.

    Returns:
        List[Dict[str, Any]]: A list of routes in dictionary form.
    """
    try:
        # Fetch all routes from the database
        # This is a placeholder for actual database retrieval logic
        all_routes = []  # Replace with actual database call
        return [route.to_dict() for route in all_routes]
    except Exception as e:
        # Log the error
        print(f"Error listing routes: {e}")
        return []

def create_route(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Business logic for creating a new route.

    Args:
        data (Dict[str, Any]): Data to create the route.

    Returns:
        Optional[Dict[str, Any]]: The created route in dictionary form, or None if creation failed.
    """
    try:
        # Validate input data
        if 'name' not in data or 'path' not in data:
            raise ValueError("Invalid data: 'name' or 'path' missing.")
        
        # Create route object
        new_route = Route.from_dict(data)
        
        # Save to the database
        # This is a placeholder for actual database save logic
        # Replace with actual database call:
        # new_route.save()
        
        return new_route.to_dict()
    except Exception as e:
        # Log the error
        print(f"Error creating route: {e}")
        return None

def edit_route(route_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Business logic for editing an existing route.

    Args:
        route_id (str): The ID of the route to edit.
        data (Dict[str, Any]): Data to update the route.

    Returns:
        Optional[Dict[str, Any]]: The updated route in dictionary form, or None if update failed.
    """
    try:
        # Fetch the route by ID
        # This is a placeholder for actual database retrieval logic
        # route = Route.get_by_id(route_id)
        
        if not route:
            raise ValueError("Route not found.")
        
        # Update route with new data
        for key, value in data.items():
            setattr(route, key, value)
        
        # Save changes to the database
        # Replace with actual database call:
        # route.save()
        
        return route.to_dict()
    except Exception as e:
        # Log the error
        print(f"Error editing route: {e}")
        return None

def remove_route(route_id: str) -> bool:
    """
    Business logic for removing a route.

    Args:
        route_id (str): The ID of the route to remove.

    Returns:
        bool: True if the route was successfully removed, False otherwise.
    """
    try:
        # Fetch the route by ID
        # This is a placeholder for actual database retrieval logic
        # route = Route.get_by_id(route_id)
        
        if not route:
            raise ValueError("Route not found.")
        
        # Remove the route from the database
        # Replace with actual database call:
        # route.delete()
        
        return True
    except Exception as e:
        # Log the error
        print(f"Error removing route: {e}")
        return False
