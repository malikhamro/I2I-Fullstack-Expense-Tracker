# auth/check_permission.py

import json
import os

PERMISSIONS_FILE = 'permissions.json'


def load_permissions():
    if not os.path.exists(PERMISSIONS_FILE):
        raise FileNotFoundError(f"Permissions file {PERMISSIONS_FILE} not found.")
    with open(PERMISSIONS_FILE, 'r') as file:
        return json.load(file)


def check_user_permission(user, action):
    """
    Verify if a user has permission to perform a specific action by checking their roles and permissions.

    :param user: dict, user object containing user roles and individual permissions
    :param action: str, the action to be checked
    :return: bool, True if the user has permission, False otherwise
    """
    try:
        permissions = load_permissions()
    except FileNotFoundError as fnf_error:
        raise PermissionError("Unable to verify permissions, permissions file is missing.") from fnf_error

    # Check user specific permissions
    user_permissions = user.get('permissions', [])
    if action in user_permissions:
        return True

    # Check user roles and their permissions
    user_roles = user.get('roles', [])
    for role in user_roles:
        role_permissions = permissions.get(role, [])
        if action in role_permissions:
            return True

    return False

def test_check_user_permission():
    # Test case setup 
    user_with_direct_permission = {
        'id': 1,
        'name': 'Alice',
        'roles': ['user'],
        'permissions': ['read']
    }

    user_with_role_permission = {
        'id': 2,
        'name': 'Bob',
        'roles': ['admin'],
        'permissions': []
    }

    user_no_permission = {
        'id': 3,
        'name': 'Charlie',
        'roles': ['guest'],
        'permissions': []
    }

    permissions = {
        'admin': ['delete', 'write', 'read'],
        'user': ['read'],
        'guest': []
    }

    def mock_load_permissions():
        return permissions

    global load_permissions
    original_load_permissions = load_permissions
    load_permissions = mock_load_permissions  # Override the actual load_permissions function with mock_load_permissions
    
    try:
        # Test user with direct permission
        assert check_user_permission(user_with_direct_permission, 'read') == True
        # Test user with role-based permission
        assert check_user_permission(user_with_role_permission, 'delete') == True
        # Test user with no permission
        assert check_user_permission(user_no_permission, 'write') == False
    finally:
        load_permissions = original_load_permissions  # Restore the original load_permissions function

# Unittest hook
if __name__ == '__main__':
    test_check_user_permission()
