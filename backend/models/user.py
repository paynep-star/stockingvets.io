from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))
    google_id = db.Column(db.String(255), unique=True)
    facebook_id = db.Column(db.String(255), unique=True)
    apple_id = db.Column(db.String(255), unique=True)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    balance = db.Column(db.Float, default=0.0)
    
    portfolio = db.relationship('Portfolio', backref='user', uselist=False, cascade='all, delete-orphan')
    verification = db.relationship('Verification', backref='user', uselist=False, cascade='all, delete-orphan')
    forum_threads = db.relationship('ForumThread', backref='author', cascade='all, delete-orphan')
    forum_responses = db.relationship('ForumResponse', backref='author', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'verified': self.verified,
            'createdAt': self.created_at.isoformat(),
            'balance': self.balance
        }
    
    def __repr__(self):
        return f'<User {self.email}>'