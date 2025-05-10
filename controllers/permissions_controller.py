# controllers/permissions_controller.py

from flask import Blueprint, request, jsonify
from services.permissions_service import (
    add_permission,
    remove_permission,
    assign_permission,
    revoke_permission,
    list_permissions,
    get_permission_by_role,
    update_permission,
)
from werkzeug.exceptions import BadRequest, NotFound

permissions_bp = Blueprint('permissions', __name__)

@permissions_bp.route('/permissions', methods=['POST'])
def create_permission():
    """Create a new permission."""
    try:
        data = request.get_json()
        if 'name' not in data or 'description' not in data:
            raise BadRequest('Missing required fields: name and description')

        permission = add_permission(data['name'], data['description'])
        return jsonify(permission), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@permissions_bp.route('/permissions/<int:permission_id>', methods=['DELETE'])
def delete_permission(permission_id):
    """Delete an existing permission."""
    try:
        remove_permission(permission_id)
        return '', 204
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@permissions_bp.route('/roles/<int:role_id>/permissions/<int:permission_id>', methods=['POST'])
def assign_permission_to_role(role_id, permission_id):
    """Assign a permission to a role."""
    try:
        assign_permission(role_id, permission_id)
        return '', 204
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@permissions_bp.route('/roles/<int:role_id>/permissions/<int:permission_id>', methods=['DELETE'])
def revoke_permission_from_role(role_id, permission_id):
    """Revoke a permission from a role."""
    try:
        revoke_permission(role_id, permission_id)
        return '', 204
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@permissions_bp.route('/permissions', methods=['GET'])
def get_permissions():
    """List all available permissions."""
    try:
        permissions = list_permissions()
        return jsonify(permissions), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@permissions_bp.route('/roles/<int:role_id>/permissions', methods=['GET'])
def get_role_permissions(role_id):
    """Retrieve permissions assigned to a specific role."""
    try:
        permissions = get_permission_by_role(role_id)
        return jsonify(permissions), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@permissions_bp.route('/permissions/<int:permission_id>', methods=['PUT'])
def update_permission_details(permission_id):
    """Update the details of a specific permission."""
    try:
        data = request.get_json()
        if 'name' not in data or 'description' not in data:
            raise BadRequest('Missing required fields: name and description')

        permission = update_permission(permission_id, data['name'], data['description'])
        return jsonify(permission), 200
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
