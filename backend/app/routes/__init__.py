"""
Route blueprints for the Code Diary application
"""
from flask import Blueprint

# Create blueprints
main_bp = Blueprint('main', __name__)
entries_bp = Blueprint('entries', __name__, url_prefix='/entries')
export_bp = Blueprint('export', __name__, url_prefix='/export')

# Import route handlers
from app.routes import main, entries, export
