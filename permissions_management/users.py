# permissions_management/users.py

from database import session
from models import UserRole, Role, User
from sqlalchemy import exc

def assign_role(user_id, role_id):
    """
    Assign a specific role to a user.

    Args:
        user_id (int): ID of the user to assign the role to.
        role_id (int): ID of the role to be assigned.

    Returns:
        dict: Success message or error information.
    """
    try:
        # Validate if user exists
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if user is None:
            return {'error': 'User not found'}

        # Validate if role exists
        role = session.query(Role).filter(Role.id == role_id).one_or_none()
        if role is None:
            return {'error': 'Role not found'}

        # Check if the role is already assigned to the user
        user_role = session.query(UserRole).filter_by(user_id=user_id, role_id=role_id).one_or_none()
        if user_role:
            return {'error': 'Role already assigned to user'}

        # Assign role to user
        new_user_role = UserRole(user_id=user_id, role_id=role_id)
        session.add(new_user_role)
        session.commit()
        return {'success': 'Role assigned successfully'}
    except exc.SQLAlchemyError as e:
        session.rollback()
        return {'error': str(e)}

def remove_role(user_id, role_id):
    """
    Remove a specific role from a user.

    Args:
        user_id (int): ID of the user from whom the role will be removed.
        role_id (int): ID of the role to be removed.

    Returns:
        dict: Success message or error information.
    """
    try:
        # Validate if user exists
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if user is None:
            return {'error': 'User not found'}

        # Validate if role exists
        role = session.query(Role).filter(Role.id == role_id).one_or_none()
        if role is None:
            return {'error': 'Role not found'}

        # Ensure the user has the role to be removed
        user_role = session.query(UserRole).filter_by(user_id=user_id, role_id=role_id).one_or_none()
        if user_role is None:
            return {'error': 'Role not assigned to user'}

        # Remove role from user
        session.delete(user_role)
        session.commit()
        return {'success': 'Role removed successfully'}
    except exc.SQLAlchemyError as e:
        session.rollback()
        return {'error': str(e)}

def list_user_roles(user_id):
    """
    List all roles assigned to a specific user.

    Args:
        user_id (int): ID of the user to list roles for.

    Returns:
        dict: List of roles or error information.
    """
    try:
        # Validate if user exists
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if user is None:
            return {'error': 'User not found'}

        # Retrieve all roles assigned to the user
        roles = session.query(Role).join(UserRole).filter(UserRole.user_id == user_id).all()
        role_list = [{'role_id': role.id, 'role_name': role.name} for role in roles]
        return {'roles': role_list}
    except exc.SQLAlchemyError as e:
        return {'error': str(e)}
