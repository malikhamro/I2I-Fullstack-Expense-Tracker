import logging
from roles.assign_role_permissions import assign_permissions_to_role

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RoleCheckError(Exception):
    """Custom exception for role checking errors."""
    pass

def check_role_validity(role_name):
    """
    Confirm whether a specified role exists and retrieve the assigned permissions.

    Args:
        role_name (str): The name of the role to check.

    Returns:
        dict: A dictionary containing role validity and permissions details.

    Raises:
        RoleCheckError: If the role does not exist or an error occurs during permission retrieval.
    """
    try:
        if not role_name:
            raise ValueError("Role name must be provided.")

        # Assuming there's a function in assign_role_permissions.py to retrieve available roles
        available_roles = assign_permissions_to_role.get_roles()
        
        if role_name not in available_roles:
            raise RoleCheckError(f"Role '{role_name}' does not exist.")

        # Retrieve permissions for the role
        permissions = assign_permissions_to_role.get_permissions_for_role(role_name)
        logger.info(f"Role '{role_name}' exists with permissions: {permissions}")

        return {
            "role_name": role_name,
            "is_valid": True,
            "permissions": permissions
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise RoleCheckError(f"Validation error: {ve}")

    except RoleCheckError as re:
        logger.warning(re)
        return {
            "role_name": role_name,
            "is_valid": False,
            "error": str(re)
        }

    except Exception as e:
        logger.error(f"An error occurred while checking role validity: {e}")
        raise RoleCheckError(f"An error occurred while checking role validity: {e}")

if __name__ == "__main__":
    # Example usage
    try:
        role_info = check_role_validity("admin")
        print(role_info)
    except RoleCheckError as e:
        print(f"Error: {e}")
