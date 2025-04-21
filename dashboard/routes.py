from flask import Blueprint, render_template, jsonify
from .controllers import get_migration_progress, get_migration_status

# Blueprint for the dashboard routes
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def render_dashboard():
    try:
        progress_data = get_migration_progress()
        status_data = get_migration_status()
    except Exception as e:
        # Logging the error message
        print(f"Error fetching data: {e}")
        progress_data = None
        status_data = None

    return render_template('dashboard.html', progress=progress_data, status=status_data)

@dashboard_bp.route('/api/migration-progress')
def migration_progress_api():
    try:
        progress_data = get_migration_progress()
        return jsonify(progress_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@dashboard_bp.route('/api/migration-status')
def migration_status_api():
    try:
        status_data = get_migration_status()
        return jsonify(status_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def init_routes(app):
    app.register_blueprint(dashboard_bp)
