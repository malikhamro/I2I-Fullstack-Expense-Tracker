# services/permissions_service.py

from models.permissions_model import Permission
from models.roles_permissions_model import RolePermission
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Here I'm assuming we are using SQLAlchemy for ORM and session management
DATABASE_URI = 'sqlite:///your_database.db'  # Change this to your actual database URI
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def add_permission(name: str, description: str):
    """Adds a new permission to the system."""
    new_permission = Permission(name=name, description=description)
    try:
        session.add(new_permission)
        session.commit()
        return new_permission.id
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding permission: {str(e)}")
        return None

def remove_permission(permission_id: int):
    """Removes a specific permission from the system."""
    try:
        permission = session.query(Permission).filter(Permission.id == permission_id).one()
        session.delete(permission)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error removing permission: {str(e)}")
        return False

def assign_permission(role_id: int, permission_id: int):
    """Assigns a specific permission to a user role."""
    new_role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
    try:
        session.add(new_role_permission)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error assigning permission to role: {str(e)}")
        return False

def revoke_permission(role_id: int, permission_id: int):
    """Revokes a specific permission from a user role."""
    try:
        role_permission = session.query(RolePermission).filter(
            RolePermission.role_id == role_id, RolePermission.permission_id == permission_id).one()
        session.delete(role_permission)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error revoking permission from role: {str(e)}")
        return False

def list_permissions():
    """Lists all permissions in the system."""
    try:
        permissions = session.query(Permission).all()
        return [(permission.id, permission.name, permission.description) for permission in permissions]
    except SQLAlchemyError as e:
        print(f"Error listing permissions: {str(e)}")
        return []

def get_permission_by_role(role_id: int):
    """Retrieves all permissions assigned to a specific user role."""
    try:
        role_permissions = session.query(RolePermission).filter(RolePermission.role_id == role_id).all()
        permission_ids = [rp.permission_id for rp in role_permissions]
        permissions = session.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        return [(permission.id, permission.name, permission.description) for permission in permissions]
    except SQLAlchemyError as e:
        print(f"Error retrieving permissions by role: {str(e)}")
        return []

def update_permission(permission_id: int, new_name: str, new_description: str):
    """Updates the details of a specific permission."""
    try:
        permission = session.query(Permission).filter(Permission.id == permission_id).one()
        permission.name = new_name
        permission.description = new_description
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating permission: {str(e)}")
        return False
