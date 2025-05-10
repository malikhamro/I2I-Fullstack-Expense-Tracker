# auth/permissions.py

import json
import os

class PermissionManager:
    def __init__(self, permission_file='permissions.json'):
        self.permission_file = permission_file
        self.permissions = self.load_permissions()

    def load_permissions(self):
        if os.path.exists(self.permission_file):
            with open(self.permission_file, 'r') as file:
                return json.load(file)
        return {}

    def save_permissions(self):
        with open(self.permission_file, 'w') as file:
            json.dump(self.permissions, file, indent=4)

    def define_permission(self, action_name, description):
        if not action_name or not description:
            raise ValueError("Action name and description cannot be empty")

        if action_name in self.permissions:
            raise ValueError("Permission already exists")

        self.permissions[action_name] = description
        self.save_permissions()

# Example usage
if __name__ == "__main__":
    pm = PermissionManager()
    try:
        pm.define_permission("read_data", "Permission to read data")
        pm.define_permission("write_data", "Permission to write data")
    except ValueError as e:
        print(e)
