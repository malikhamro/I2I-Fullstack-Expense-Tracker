from flask import Blueprint, request, jsonify
from api.models import ResourceModel, db
from api.schemas import ResourceSchema

resource_bp = Blueprint('resources', __name__)

@resource_bp.route('/resources', methods=['GET'])
def get_resources():
    try:
        resources = ResourceModel.query.all()
        schema = ResourceSchema(many=True)
        result = schema.dump(resources)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resource_bp.route('/resources/<int:id>', methods=['GET'])
def get_resource(id):
    try:
        resource = ResourceModel.query.get_or_404(id)
        schema = ResourceSchema()
        result = schema.dump(resource)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resource_bp.route('/resources', methods=['POST'])
def create_resource():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validate and deserialize input
        schema = ResourceSchema()
        data = schema.load(json_data)
        
        # Create new resource
        new_resource = ResourceModel(**data)
        db.session.add(new_resource)
        db.session.commit()
        
        result = schema.dump(new_resource)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resource_bp.route('/resources/<int:id>', methods=['PUT'])
def update_resource(id):
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Fetch resource to update
        resource = ResourceModel.query.get_or_404(id)
        
        # Validate and deserialize input
        schema = ResourceSchema()
        data = schema.load(json_data)
        
        # Update resource fields
        for key, value in data.items():
            setattr(resource, key, value)
        
        db.session.commit()
        
        result = schema.dump(resource)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resource_bp.route('/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
    try:
        resource = ResourceModel.query.get_or_404(id)
        db.session.delete(resource)
        db.session.commit()
        return jsonify({"message": "Resource deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
