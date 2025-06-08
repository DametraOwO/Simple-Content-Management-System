from core.models.base import BaseModel
from core.database import db

class Content(BaseModel):
    __tablename__ = 'contents'
    
    title = db.Column(db.String(255), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Content {self.title}>'
    
    @classmethod
    def get_by_user(cls, user_id):
        """Get all contents for a specific user"""
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_published(cls):
        """Get all published contents"""
        return cls.query.filter_by(status='Published').all()
    
    @classmethod
    def get_drafts(cls):
        """Get all draft contents"""
        return cls.query.filter_by(status='Draft').all()
    
    def to_dict(self):
        data = super().to_dict()
        data['author'] = self.author.username if self.author else None
        return data 