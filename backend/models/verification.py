from app import db
from datetime import datetime
import uuid

class Verification(db.Model):
    __tablename__ = 'verifications'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    id_document_url = db.Column(db.String(255), nullable=True)
    twitter_handle = db.Column(db.String(120), nullable=True)
    discord_username = db.Column(db.String(120), nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewer_notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'fullName': self.full_name,
            'dateOfBirth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'twitterHandle': self.twitter_handle,
            'discordUsername': self.discord_username,
            'linkedinUrl': self.linkedin_url,
            'status': self.status,
            'createdAt': self.created_at.isoformat(),
            'reviewedAt': self.reviewed_at.isoformat() if self.reviewed_at else None
        }
    
    def __repr__(self):
        return f'<Verification {self.user_id}>'