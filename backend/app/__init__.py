"""
Flask application factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import config

db = SQLAlchemy()

def create_app(config_name='development'):
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/templates')),
                static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/static')))
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Import and register blueprints
    from app.routes import main_bp, entries_bp, export_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(entries_bp)
    app.register_blueprint(export_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
