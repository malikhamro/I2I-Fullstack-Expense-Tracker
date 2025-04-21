from flask import Flask, jsonify
from config_ui.routes import create_routes

def create_app_instance():
    """
    Creates and configures the Flask application instance.

    Returns:
        Flask: The configured Flask application instance.
    """
    # Instantiate the Flask application
    app = Flask(__name__)

    # Set up configurations (this can be extended with specific configuration settings)
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure key for production usage
    app.config['DEBUG'] = True  # Enable debugging for development

    # Register blueprints or extensions here (if any)
    create_routes(app)

    # Error handler for 404 errors
    @app.errorhandler(404)
    def page_not_found(e):
        # Respond with JSON for 404 errors
        return jsonify(error="Resource not found"), 404

    # Error handler for 500 errors
    @app.errorhandler(500)
    def internal_server_error(e):
        # Respond with JSON for 500 errors
        return jsonify(error="Internal server error"), 500

    return app

if __name__ == "__main__":
    app = create_app_instance()
    app.run(host='0.0.0.0', port=5000)
