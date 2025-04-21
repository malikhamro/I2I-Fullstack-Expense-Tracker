# File: authentication/rbac.py

class RBAC:
    def __init__(self):
        self.roles = {}
        self.user_roles = {}
        self.role_permissions = {}

    def initialize_roles(self):
        """
        Initializes predefined roles and their respective permissions.
        Sets up roles such as 'admin', 'user', and 'guest', 
        and defines what each role can access.
        """
        self.roles = {
            'admin': ['create', 'read', 'update', 'delete'],
            'user': ['read', 'update'],
            'guest': ['read']
        }
        self.role_permissions = {
            'create': ['admin'],
            'read': ['admin', 'user', 'guest'],
            'update': ['admin', 'user'],
            'delete': ['admin']
        }
    
    def assign_role(self, user_id, role):
        """
        Assigns a specified role to a user.
        
        Parameters:
        - user_id: Unique identifier for the user
        - role: The role to assign to the user
        """
        if role not in self.roles:
            raise ValueError(f"Role {role} does not exist.")
        
        if user_id in self.user_roles:
            self.user_roles[user_id].add(role)
        else:
            self.user_roles[user_id] = {role}

    def check_permission(self, user_id, permission):
        """
        Checks if the user has the necessary permission.
        
        Parameters:
        - user_id: Unique identifier for the user
        - permission: The permission to check
        
        Returns:
        - True if the user has the permission, False otherwise
        """
        user_roles = self.user_roles.get(user_id, set())
        for role in user_roles:
            if permission in self.roles.get(role, []):
                return True
        return False

    def revoke_role(self, user_id, role):
        """
        Revokes a specified role from a user.
        
        Parameters:
        - user_id: Unique identifier for the user
        - role: The role to revoke from the user
        """
        if user_id in self.user_roles:
            self.user_roles[user_id].discard(role)
            if not self.user_roles[user_id]:
                del self.user_roles[user_id]

# Example Usage
if __name__ == "__main__":
    rbac = RBAC()
    rbac.initialize_roles()

    # Assign role to a user
    rbac.assign_role('user123', 'admin')
    rbac.assign_role('user123', 'user')

    # Check permission
    print(rbac.check_permission('user123', 'create')) # True
    print(rbac.check_permission('user123', 'delete')) # True
    print(rbac.check_permission('user123', 'read'))   # True

    # Revoke role
    rbac.revoke_role('user123', 'admin')
    print(rbac.check_permission('user123', 'delete')) # False
