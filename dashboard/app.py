from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configuration settings
    app.config.from_object('config.Config')
    
    # Initialize plugins
    db.init_app(app)
    
    # Register routes
    from .routes import init_routes
    init_routes(app)
    
    return app

# Configuration for the Flask app (in a separate config.py file)
class Config:
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
