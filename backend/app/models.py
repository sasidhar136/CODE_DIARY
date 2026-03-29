"""
Database models for the Code Diary application
"""
from app import db
import sqlalchemy as sa
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """Model for storing user accounts"""
    __tablename__ = 'user'
    
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(64), index=True, unique=True, nullable=False)
    email = sa.Column(sa.String(120), index=True, unique=True, nullable=False)
    password_hash = sa.Column(sa.String(256))
    
    # Relationship to entries
    entries = db.relationship('Entry', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<User {self.username}>'

class Entry(db.Model):
    """Model for storing learning diary entries"""
    __tablename__ = 'entry'
    
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.Text, nullable=False)
    timestamp = sa.Column(sa.DateTime, default=datetime.utcnow)
    summary = sa.Column(sa.Text, nullable=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Entry {self.id}>'
    
    def to_dict(self):
        """Convert entry to dictionary"""
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'summary': self.summary,
            'user_id': self.user_id
        }
