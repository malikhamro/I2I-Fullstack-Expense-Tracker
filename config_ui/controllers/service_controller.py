from flask import Blueprint, jsonify, request
from config_ui.services.service_service import (
    list_services,
    create_service,
    edit_service,
    remove_service
)

# Create a Blueprint for service management
service_blueprint = Blueprint('service', __name__)

# Handle getting the list of services
@service_blueprint.route('/services', methods=['GET'])
def get_services():
    try:
        services = list_services()
        return jsonify([service.to_dict() for service in services]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Handle adding a new service
@service_blueprint.route('/services', methods=['POST'])
def add_service():
    try:
        service_data = request.get_json()
        create_service(service_data)
        return jsonify({'message': 'Service added successfully'}), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Handle updating an existing service
@service_blueprint.route('/services/<service_id>', methods=['PUT'])
def update_service(service_id):
    try:
        service_data = request.get_json()
        edit_service(service_id, service_data)
        return jsonify({'message': 'Service updated successfully'}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Handle deleting a service
@service_blueprint.route('/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    try:
        remove_service(service_id)
        return jsonify({'message': 'Service deleted successfully'}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
