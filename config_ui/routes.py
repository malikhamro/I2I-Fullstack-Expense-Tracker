from flask import Blueprint
from config_ui.controllers.route_controller import get_routes, add_route, update_route, delete_route
from config_ui.controllers.policy_controller import get_policies, add_policy, update_policy, delete_policy
from config_ui.controllers.service_controller import get_services, add_service, update_service, delete_service

def create_routes():
    routes_bp = Blueprint('routes', __name__)

    # Route endpoints
    routes_bp.route('/routes', methods=['GET'])(get_routes)
    routes_bp.route('/routes', methods=['POST'])(add_route)
    routes_bp.route('/routes/<int:route_id>', methods=['PUT'])(update_route)
    routes_bp.route('/routes/<int:route_id>', methods=['DELETE'])(delete_route)

    # Policy endpoints
    routes_bp.route('/policies', methods=['GET'])(get_policies)
    routes_bp.route('/policies', methods=['POST'])(add_policy)
    routes_bp.route('/policies/<int:policy_id>', methods=['PUT'])(update_policy)
    routes_bp.route('/policies/<int:policy_id>', methods=['DELETE'])(delete_policy)

    # Service endpoints
    routes_bp.route('/services', methods=['GET'])(get_services)
    routes_bp.route('/services', methods=['POST'])(add_service)
    routes_bp.route('/services/<int:service_id>', methods=['PUT'])(update_service)
    routes_bp.route('/services/<int:service_id>', methods=['DELETE'])(delete_service)

    return routes_bp
