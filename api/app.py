from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize database instance
db = SQLAlchemy()
migrate = Migrate()

def register_extensions(app: Flask):
    """
    Registers extensions to the Flask app.
    """
    db.init_app(app)
    migrate.init_app(app, db)

def register_blueprints(app: Flask):
    """
    Registers blueprints to the Flask app.
    """
    from api.routes.resource_routes import resource_bp
    app.register_blueprint(resource_bp, url_prefix='/api')

def configure_logging(app: Flask):
    """
    Configures logging for the Flask app.
    """
    log_dir = app.config.get('LOG_DIRECTORY', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    file_handler = RotatingFileHandler(os.path.join(log_dir, 'app.log'), maxBytes=100000, backupCount=10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] - %(message)s'
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

def create_app(config_name=None):
    """
    Create and configure the Flask app.
    """
    app = Flask(__name__)

    # Load configuration
    if config_name:
        app.config.from_object(config_name)
    else:
        app.config.from_pyfile('config.py')

    # Register extensions
    register_extensions(app)

    # Register blueprints for routes
    register_blueprints(app)

    # Configure logging
    configure_logging(app)

    return app
