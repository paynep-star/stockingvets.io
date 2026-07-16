from app import db
from datetime import datetime
import uuid

class ForumThread(db.Model):
    __tablename__ = 'forum_threads'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    
    responses = db.relationship('ForumResponse', backref='thread', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author.name,
            'title': self.title,
            'content': self.content,
            'preview': self.content[:100] + '...' if len(self.content) > 100 else self.content,
            'createdAt': self.created_at.isoformat(),
            'views': self.views,
            'responseCount': len(self.responses)
        }
    
    def __repr__(self):
        return f'<ForumThread {self.title}>'

class ForumResponse(db.Model):
    __tablename__ = 'forum_responses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    thread_id = db.Column(db.String(36), db.ForeignKey('forum_threads.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'threadId': self.thread_id,
            'author': self.author.name,
            'content': self.content,
            'createdAt': self.created_at.isoformat(),
            'likes': self.likes
        }
    
    def __repr__(self):
        return f'<ForumResponse {self.id}>'