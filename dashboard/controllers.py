# dashboard/controllers.py

from flask import jsonify
from .models import MigrationProgress, MigrationStatus
from sqlalchemy.exc import SQLAlchemyError

def get_migration_progress():
    """
    Fetches the migration progress data from the database.
    This function will be used by the route handling function in routes.py:init_routes.
    """
    try:
        progress_data = MigrationProgress.query.all()
        if not progress_data:
            return jsonify({"error": "No migration progress data found"}), 404
        
        formatted_data = [progress.to_dict() for progress in progress_data]
        return jsonify({"migration_progress": formatted_data}), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

def get_migration_status():
    """
    Fetches the current status of the migration process.
    This function will be used by the route handling function in routes.py:init_routes.
    """
    try:
        status_data = MigrationStatus.query.first()
        if not status_data:
            return jsonify({"error": "No migration status data found"}), 404
        
        return jsonify({"migration_status": status_data.to_dict()}), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
