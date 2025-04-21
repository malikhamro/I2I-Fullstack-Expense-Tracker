# services/user_service.py

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dummy data for user-role mapping for illustration purposes
user_role_mapping = {
    1: ['admin', 'user'],
    2: ['user'],
    3: ['guest'],
}

class UserService:
    @staticmethod
    def get_user_roles(user_id):
        """
        This function retrieves the roles assigned to a specific user.
        It communicates with the role-based access module to fetch user roles.
        
        :param user_id: The ID of the user
        :return: A list of roles assigned to the user or an empty list if the user ID does not exist
        """
        try:
            if user_id in user_role_mapping:
                roles = user_role_mapping[user_id]
                logger.info(f"Roles for user_id {user_id}: {roles}")
                return roles
            else:
                logger.warning(f"User ID {user_id} not found.")
                return []
        except Exception as e:
            logger.error(f"An error occurred while fetching roles for user_id {user_id}: {str(e)}")
            return []

# Sample usage
if __name__ == "__main__":
    user_id = 1
    user_roles = UserService.get_user_roles(user_id)
    print(f"Roles for user ID {user_id}: {user_roles}")
