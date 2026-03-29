"""
Entry management routes
"""
from flask import render_template, redirect, request, url_for, flash
from datetime import datetime, timedelta
from flask_login import login_required, current_user
from app.routes import entries_bp
from app.models import Entry
from app import db
from app.utils.ai_summary import get_ai_summary

@entries_bp.route('/new')
@login_required
def new_entry():
    """Show new entry form"""
    return render_template('input.html', now=datetime.now)

@entries_bp.route('/add', methods=['POST'])
@login_required
def add_entry():
    """Add a new entry"""
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if not content:
            flash('Your learning entry cannot be empty!', 'danger')
            return redirect(url_for('entries.new_entry'))
    
    summary = get_ai_summary(content)
    new_entry = Entry(content=content, summary=summary, user_id=current_user.id)
    
    try:
        db.session.add(new_entry)
        db.session.commit()
        message = 'Your entry is saved successfully!'
        if summary:
            message += ' (with AI summary!)'
        else:
            message += ' (AI summary failed to generate.)'
        flash(message, 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while saving: {e}', 'danger')
    
    return redirect(url_for('entries.new_entry'))

@entries_bp.route('/clear', methods=['POST'])
@login_required
def clear_all_entries():
    """Clear all entries for the current user"""
    try:
        num_deleted = db.session.query(Entry).filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash(f'Successfully deleted {num_deleted} entries!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while clearing entries: {e}', 'danger')
    return redirect(url_for('main.dashboard'))

@entries_bp.route('/weekly-summary')
@login_required
def weekly_summary():
    """Show weekly summary of entries for the current user"""
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_entries = Entry.query.filter(
        Entry.user_id == current_user.id,
        Entry.timestamp >= seven_days_ago
    ).order_by(Entry.timestamp.asc()).all()

    combined_content = ""
    for entry in recent_entries:
        combined_content += f"On {entry.timestamp.strftime('%Y-%m-%d')}: {entry.content}\n\n"

    weekly_summary_text = None
    if combined_content.strip():
        prompt = (
            "Generate a concise, high-level summary (3-5 sentences) of the following "
            "weekly technical learning entries. Focus on overarching themes, key "
            "technologies mentioned, and significant achievements:\n\n"
            f"{combined_content}"
        )
        weekly_summary_text = get_ai_summary(prompt)
    
    return render_template('weekly_summary.html', 
                         weekly_summary=weekly_summary_text,
                         now=datetime.now)
