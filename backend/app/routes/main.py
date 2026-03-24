"""
Main routes for the Code Diary application
"""
from flask import render_template, redirect, url_for
from app.routes import main_bp

@main_bp.route('/')
def index():
    """Home page - redirects to new entry"""
    return redirect(url_for('entries.new_entry'))

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard route - shows all entries"""
    from app.models import Entry
    from datetime import datetime, timedelta
    
    entries = Entry.query.order_by(Entry.timestamp.desc()).all()
    return render_template('dashboard.html', 
                         entries=entries, 
                         now=datetime.now, 
                         timedelta=timedelta)
