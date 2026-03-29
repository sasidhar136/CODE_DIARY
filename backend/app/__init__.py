"""
Flask application factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app(config_name='development'):
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/templates')),
                static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/static')))
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)
    
    # Import and register blueprints
    from app.routes.main import main_bp
    from app.routes.entries import entries_bp
    from app.routes.export import export_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(entries_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(auth_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
