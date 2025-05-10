# roles/assign_role_permissions.py

import json

class RolePermissionAssigner:
    def __init__(self, permissions_file='permissions.json', roles_permissions_file='roles_permissions.json'):
        self.permissions_file = permissions_file
        self.roles_permissions_file = roles_permissions_file
        self.permissions = self._load_permissions()
        self.roles_permissions = self._load_roles_permissions()

    def _load_permissions(self):
        try:
            with open(self.permissions_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _load_roles_permissions(self):
        try:
            with open(self.roles_permissions_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_roles_permissions(self):
        with open(self.roles_permissions_file, 'w') as file:
            json.dump(self.roles_permissions, file, indent=4)

    def assign_permissions_to_role(self, role, permissions):
        if role not in self.roles_permissions:
            self.roles_permissions[role] = []
        
        for permission in permissions:
            if permission in self.permissions:
                if permission not in self.roles_permissions[role]:
                    self.roles_permissions[role].append(permission)
            else:
                raise ValueError(f"Permission '{permission}' does not exist.")

        self._save_roles_permissions()

    def get_role_permissions(self, role):
        return self.roles_permissions.get(role, [])

    def define_permission(self, permission_name, description):
        if permission_name in self.permissions:
            raise ValueError(f"Permission '{permission_name}' already exists.")
        self.permissions[permission_name] = description
        self._save_permissions()

    def _save_permissions(self):
        with open(self.permissions_file, 'w') as file:
            json.dump(self.permissions, file, indent=4)

# Example usage
if __name__ == "__main__":
    role_permission_assigner = RolePermissionAssigner()
    
    # Defining some permissions first
    role_permission_assigner.define_permission("edit_article", "Permission to edit an article")
    role_permission_assigner.define_permission("delete_article", "Permission to delete an article")
    
    # Assigning those permissions to a role
    role_permission_assigner.assign_permissions_to_role("editor", ["edit_article", "delete_article"])
    
    # Retrieving assigned permissions for a role
    editor_permissions = role_permission_assigner.get_role_permissions("editor")
    print(f"Permissions for role 'editor': {editor_permissions}")
