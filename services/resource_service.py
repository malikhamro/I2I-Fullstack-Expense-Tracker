# services/resource_service.py

# Import necessary modules
import logging
from authentication.rbac import check_permission

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def access_resource(user_id, resource):
    """
    This function manages resource access requests. 
    It uses the check_permission function from authentication/rbac.py to determine if the user can access the resource.

    :param user_id: ID of the user attempting to access the resource
    :param resource: The resource the user is attempting to access
    :return: True if access is granted, False otherwise
    """
    try:
        # Check if the user has permission to access the resource
        has_permission = check_permission(user_id, resource)
        
        if has_permission:
            logger.info(f"Access granted for user {user_id} to resource {resource}")
            return True
        else:
            logger.warning(f"Access denied for user {user_id} to resource {resource}")
            return False

    except Exception as e:
        # Log any errors that occur during the process
        logger.error(f"An error occurred while checking permission for user {user_id} to access resource {resource}: {str(e)}")
        return False

