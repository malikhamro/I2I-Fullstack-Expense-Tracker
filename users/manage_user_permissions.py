import json
from roles.assign_role_permissions import assign_permissions_to_role

class UserPermissionManager:
    def __init__(self, user_permissions_file='user_permissions.json'):
        self.user_permissions_file = user_permissions_file
        self.permissions_data = self.load_permissions()

    def load_permissions(self):
        """ Load user permissions from a JSON file. """
        try:
            with open(self.user_permissions_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            raise Exception(f"Error decoding JSON from {self.user_permissions_file}: {e}")

    def save_permissions(self):
        """ Save user permissions to a JSON file. """
        try:
            with open(self.user_permissions_file, 'w') as file:
                json.dump(self.permissions_data, file, indent=4)
        except IOError as e:
            raise Exception(f"Error writing to {self.user_permissions_file}: {e}")

    def assign_permissions_to_user(self, user_id, permissions, override_role_permissions=False):
        """
        Assign specific permissions to an individual user, optionally overriding role-based permissions.
        
        :param user_id: ID of the user to assign permissions to.
        :param permissions: List of permissions to assign to the user.
        :param override_role_permissions: Boolean indicating whether to override role-based permissions.
        :return: None
        """
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id must be a non-empty string.")

        if not isinstance(permissions, list) or not all(isinstance(p, str) for p in permissions):
            raise ValueError("permissions must be a list of non-empty strings.")

        if not isinstance(override_role_permissions, bool):
            raise ValueError("override_role_permissions must be a boolean.")

        # Fetch default role permissions if override is not specified
        if not override_role_permissions:
            default_role_permissions = assign_permissions_to_role(user_id)
            permissions = list(set(default_role_permissions + permissions))

        self.permissions_data[user_id] = permissions
        self.save_permissions()

    def get_user_permissions(self, user_id):
        """
        Retrieve permissions for a specified user.
        
        :param user_id: ID of the user for whom to retrieve permissions.
        :return: List of permissions assigned to the user.
        """
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id must be a non-empty string.")
        
        return self.permissions_data.get(user_id, [])

# Example Usage:
# user_permission_manager = UserPermissionManager()
# user_permission_manager.assign_permissions_to_user("user123", ["read", "write"], True)
# print(user_permission_manager.get_user_permissions("user123"))
