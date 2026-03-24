"""
Database models for the Code Diary application
"""
from app import db
from datetime import datetime

class Entry(db.Model):
    """Model for storing learning diary entries"""
    __tablename__ = 'entry'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    summary = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Entry {self.id}>'
    
    def to_dict(self):
        """Convert entry to dictionary"""
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'summary': self.summary
        }
