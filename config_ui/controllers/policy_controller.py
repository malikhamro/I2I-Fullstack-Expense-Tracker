from flask import Blueprint, jsonify, request
from config_ui.services.policy_service import list_policies, create_policy, edit_policy, remove_policy

policy_controller = Blueprint('policy_controller', __name__)

@policy_controller.route('/policies', methods=['GET'])
def get_policies():
    try:
        policies = list_policies()
        return jsonify(policies), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@policy_controller.route('/policies', methods=['POST'])
def add_policy():
    try:
        policy_data = request.json
        new_policy = create_policy(policy_data)
        return jsonify(new_policy), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@policy_controller.route('/policies/<policy_id>', methods=['PUT'])
def update_policy(policy_id):
    try:
        policy_data = request.json
        updated_policy = edit_policy(policy_id, policy_data)
        if updated_policy:
            return jsonify(updated_policy), 200
        else:
            return jsonify({'error': 'Policy not found'}), 404
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@policy_controller.route('/policies/<policy_id>', methods=['DELETE'])
def delete_policy(policy_id):
    try:
        result = remove_policy(policy_id)
        if result:
            return jsonify({'message': 'Policy deleted successfully'}), 200
        else:
            return jsonify({'error': 'Policy not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
