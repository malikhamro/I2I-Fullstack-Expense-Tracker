# roles.py

import sqlite3
from typing import List

# Constants for database connections
DB_PATH = "permissions_management.db"  # Assume the database path

class RoleManagementError(Exception):
    pass

class RoleManagement:
    
    @staticmethod
    def create_role(role_name: str) -> None:
        """
        Allows the admin to create a new role.
        Takes role_name as input and adds this new role to the roles database.
        
        :param role_name: Name of the role to be created
        :raises RoleManagementError: If the role creation fails
        """
        if not role_name:
            raise ValueError("Role name cannot be empty.")
        
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            
            # Check if the role already exists
            cursor.execute("SELECT COUNT(*) FROM roles WHERE role_name = ?", (role_name,))
            if cursor.fetchone()[0] > 0:
                raise RoleManagementError(f"Role '{role_name}' already exists.")
            
            # Insert new role into roles table
            cursor.execute("INSERT INTO roles (role_name) VALUES (?)", (role_name,))
            connection.commit()
        except sqlite3.Error as e:
            raise RoleManagementError(f"Failed to create role '{role_name}'. Error: {str(e)}")
        finally:
            connection.close()
    
    @staticmethod
    def delete_role(role_id: int) -> None:
        """
        Allows the admin to delete an existing role.
        Takes role_id as input and removes the role from both the roles and permissions databases.

        :param role_id: ID of the role to be deleted
        :raises RoleManagementError: If the role deletion fails
        """
        if role_id <= 0:
            raise ValueError("Invalid role ID.")
        
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            
            # Delete the role from the roles table
            cursor.execute("DELETE FROM roles WHERE role_id = ?", (role_id,))
            
            # Remove associated permissions
            cursor.execute("DELETE FROM role_permissions WHERE role_id = ?", (role_id,))
            connection.commit()
            
            if cursor.rowcount == 0:
                raise RoleManagementError(f"No role found with ID '{role_id}' to delete.")
                
        except sqlite3.Error as e:
            raise RoleManagementError(f"Failed to delete role with ID '{role_id}'. Error: {str(e)}")
        finally:
            connection.close()
    
    @staticmethod
    def list_roles() -> List[str]:
        """
        Displays all roles within the system by querying the roles database.

        :return: List of role names
        :raises RoleManagementError: If there is an error retrieving the roles
        """
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            
            # Retrieve all roles
            cursor.execute("SELECT role_name FROM roles")
            roles = [row[0] for row in cursor.fetchall()]
            
            return roles
        
        except sqlite3.Error as e:
            raise RoleManagementError(f"Failed to retrieve roles. Error: {str(e)}")
        finally:
            connection.close()
