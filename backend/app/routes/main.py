"""
Main routes for the Code Diary application
"""
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.routes import main_bp

@main_bp.route('/')
def index():
    """Home page - redirects to new entry"""
    return redirect(url_for('entries.new_entry'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard route - shows all entries for current user"""
    from app.models import Entry
    from datetime import datetime, timedelta
    
    entries = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.timestamp.desc()).all()
    return render_template('dashboard.html', 
                         entries=entries, 
                         now=datetime.now, 
                         timedelta=timedelta)
