from flask import Blueprint, request, jsonify
from services.route_service import list_routes, create_route, edit_route, remove_route
from models.route_model import Route, from_dict, to_dict

# Create a Blueprint for routes
route_bp = Blueprint('routes', __name__)

@route_bp.route('/routes', methods=['GET'])
def get_routes():
    try:
        routes = list_routes()
        return jsonify([to_dict(route) for route in routes]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@route_bp.route('/routes', methods=['POST'])
def add_route():
    try:
        data = request.json
        route = from_dict(data)
        create_route(route)
        return jsonify(to_dict(route)), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@route_bp.route('/routes/<route_id>', methods=['PUT'])
def update_route(route_id):
    try:
        data = request.json
        route = from_dict(data)
        route.id = route_id
        edit_route(route)
        return jsonify(to_dict(route)), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@route_bp.route('/routes/<route_id>', methods=['DELETE'])
def delete_route(route_id):
    try:
        remove_route(route_id)
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
