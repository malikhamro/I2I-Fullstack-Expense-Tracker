# api_gateway/app.py

from flask import Flask, jsonify
from gateway import register_routes
import logging

app = Flask(__name__)

def initialize_gateway():
    # Setting up logging
    logging.basicConfig(level=logging.INFO)
    
    app.logger.info("Initializing API Gateway...")
    
    # Middleware setup
    @app.before_request
    def before_request():
        app.logger.info("Before request middleware executed")

    @app.after_request
    def after_request(response):
        app.logger.info("After request middleware executed")
        return response

    # Error handling
    @app.errorhandler(404)
    def not_found(error):
        app.logger.error("404 Not Found: %s", (str(error)))
        return jsonify({"error": "Not Found"}), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error("500 Internal Server Error: %s", (str(error)))
        return jsonify({"error": "Internal Server Error"}), 500

    app.logger.info("Registering routes dynamically...")
    
    # Register routes dynamically
    try:
        register_routes(app)
    except Exception as e:
        app.logger.error("Error while registering routes: %s", str(e))
        raise e

    app.logger.info("API Gateway initialization completed successfully.")
    
if __name__ == "__main__":
    initialize_gateway()
    app.run(host='0.0.0.0', port=5000)
