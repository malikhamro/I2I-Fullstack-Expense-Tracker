# permissions_management/permissions.py

import sqlite3
from typing import List

DATABASE = 'permissions_management.db'

def db_connect():
    """ Create a database connection to the SQLite database specified by DATABASE """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        print(e)
    return conn

def add_permission(role_id: int, permission: str) -> bool:
    """
    Add a specific permission to a role.
    
    :param role_id: ID of the role
    :param permission: Permission string to be added to the role
    :return: True if permission is added successfully, False otherwise
    """
    try:
        conn = db_connect()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        
        # Check if the permission already exists for the role
        cursor.execute("SELECT * FROM role_permissions WHERE role_id = ? AND permission = ?", (role_id, permission))
        existing_permission = cursor.fetchone()

        if existing_permission:
            print(f"Permission '{permission}' already exists for role ID {role_id}.")
            return False
        
        # Insert the new permission for the role
        cursor.execute("INSERT INTO role_permissions (role_id, permission) VALUES (?, ?)", (role_id, permission))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()

def remove_permission(role_id: int, permission: str) -> bool:
    """
    Remove a specific permission from a role.
    
    :param role_id: ID of the role
    :param permission: Permission string to be removed from the role
    :return: True if permission is removed successfully, False otherwise
    """
    try:
        conn = db_connect()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        
        # Check if the permission exists for the role
        cursor.execute("SELECT * FROM role_permissions WHERE role_id = ? AND permission = ?", (role_id, permission))
        existing_permission = cursor.fetchone()

        if not existing_permission:
            print(f"Permission '{permission}' does not exist for role ID {role_id}.")
            return False
        
        # Remove the permission for the role
        cursor.execute("DELETE FROM role_permissions WHERE role_id = ? AND permission = ?", (role_id, permission))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()

def list_permissions(role_id: int) -> List[str]:
    """
    Display all the permissions assigned to a specific role.
    
    :param role_id: ID of the role
    :return: List of permissions assigned to the role
    """
    try:
        conn = db_connect()
        if conn is None:
            return []
        
        cursor = conn.cursor()
        
        # Retrieve all permissions for the role
        cursor.execute("SELECT permission FROM role_permissions WHERE role_id = ?", (role_id,))
        permissions = cursor.fetchall()
        return [permission[0] for permission in permissions]
    except sqlite3.Error as e:
        print(e)
        return []
    finally:
        if conn:
            conn.close()
